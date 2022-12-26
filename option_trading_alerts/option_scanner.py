from option_trading_alerts import discord_conn
from option_trading_alerts import td_conn
from option_trading_alerts import db_conn

from dotenv import load_dotenv

load_dotenv()


async def scan_option_prices():
    ticker = option_type = option_strike_price = option_expire_date = None
    while not ticker:
        ticker, option_type, option_strike_price, option_expire_date = await discord_conn.run_discord_client()



    # asset_premium = td_conn.get_asset_info(ticker, option_type, option_strike_price, option_expire_date)
    print(asset_premium)


if __name__ == '__main__':
    scan_option_prices()