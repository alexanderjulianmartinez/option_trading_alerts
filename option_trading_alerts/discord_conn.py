import os
import discord
from dotenv import load_dotenv

import option_trading_alerts.td_conn as td_conn

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL_ID_1')


def month_abrv_mapping(month):
    month_map = {
        'JAN': '01',
        'FEB': '02',
        'MAR': '03',
        'APR': '04',
        'MAY': '05',
        'JUN': '06',
        'JUL': '07',
        'AUG': '08',
        'SEP': '09',
        'OCT': '10',
        'NOV': '11',
        'DEC': '12',
    }
    return month_map[month.upper()]


class DiscordConnClient(discord.Client):

    @staticmethod
    def parse_alert(message_content):
        if not message_content:
            return None
        ticker = asset_strike_price = asset_expire_date = option_type = option_strike = None
        month_idx = year_idx = asset_price_idx = None
        option_str_list = ['Call', 'C', 'P', 'Put']
        message_content_list = message_content.split(' ')
        for i, content in enumerate(message_content_list):
            message_str = str(content)
            if not message_str.isalnum():
                continue
            elif message_str in option_str_list:
                if message_str in ['Call', 'C']:
                    option_type = 'CALL'
                else:
                    option_type = 'PUT'
                asset_price_idx = i + 1
            elif message_str.isupper():
                ticker = message_str
                print(f'Ticker is: {ticker}')
            else:
                month_prefix_list = [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ]
                if message_str in ['2022', '2023', '2024']:
                    year_idx = i

                else:
                    for month_prefix in month_prefix_list:
                        if message_str.startswith(month_prefix):
                            month_idx = i

        if month_idx and year_idx:
            strike_idx = year_idx + 1
            option_strike = message_content_list[strike_idx] + '.0'
            print(f'The strike price is: {option_strike}')
            asset_expire_date = ' '.join(message_content_list[month_idx: year_idx + 1])
            if asset_price_idx:
                asset_strike_price = str(message_content_list[asset_price_idx]).lstrip("@")
                print(f'Asset alert price: {asset_strike_price}')
            print(f'Asset expire date: {asset_expire_date}')

        if ticker and asset_strike_price and asset_expire_date:

            return ticker, option_type, option_strike, asset_expire_date
        else:
            return None, None, None, None

    async def get_src_msg_content(self, ref_msg):
        src_msg = self.get_guild(DISCORD_CHANNEL).get_channel().fetch_message(ref_msg.id)
        return src_msg.content

    async def on_ready(self):
        print(
            f'{self.user} is connected to Discord and scanning for option trading alerts...\n'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return None

        if 'Call @' in message.content or 'C @' in message.content:
            print(f'Call Option Alert: {message.content}')
            ticker, option_type, option_strike_price, option_expire_date = self.parse_alert(message.content)
            # print(ticker, option_type, option_strike_price, option_expire_date)
            if not ticker or not option_strike_price or not option_expire_date:
                print('Failed to parse alert data...')
            else:
                print([ticker, option_type, option_strike_price, option_expire_date])
                option_year = option_expire_date.split(' ')[-1]
                option_month = month_abrv_mapping(option_expire_date.split(' ')[0])
                if len(option_expire_date.split(' ')[1]) > 1:
                    option_day = option_expire_date.split(' ')[1]
                else:
                    option_day = '0' + option_expire_date.split(' ')[1]
                new_option_expire_date = option_year + '-' + str(option_month) + '-' + option_day
                asset_premium = td_conn.get_asset_info(ticker, option_type, option_strike_price, new_option_expire_date)
                print(asset_premium)

        elif 'Put @' in message.content or 'P @' in message.content:
            print(f'Put Option Alert: {message.content}')
            ticker, option_type, option_strike_price, option_expire_date = self.parse_alert(message.content)
            if not ticker or not option_strike_price or not option_expire_date:
                print('Failed to parse alert data...')
            else:
                print([ticker, option_type, option_strike_price, option_expire_date])
                option_year = option_expire_date.split(' ')[-1]
                option_month = month_abrv_mapping(option_expire_date.split(' ')[0])
                if len(option_expire_date.split(' ')[1]) > 1:
                    option_day = option_expire_date.split(' ')[1]
                else:
                    option_day = '0' + option_expire_date.split(' ')[1]
                new_option_expire_date = option_year + '-' + str(option_month) + '-' + option_day
                asset_premium = await td_conn.get_asset_info(ticker, option_type, option_strike_price, new_option_expire_date)
                print(asset_premium)

        else:
            print(f'Follow up alert: {message.content}')
            # src_message_content = await self.get_src_msg_content(message.reference)
            # print(f'Original alert: {src_message_content}')


def run_discord_client():
    client = DiscordConnClient()
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_discord_client()
