import os
import json
# TODO: requests is not compatible with asyncio (e.g. discord bot's async functions
#  and await calls
import requests
import datetime

from dotenv import load_dotenv
from datetime import date

load_dotenv()
td_consumer_key = os.getenv('TD_TOKEN')

endpoint_base = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'


def get_asset_info(ticker, option_type, strike_price, expire_date):
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType=' \
               '{contract_type}&fromDate={expire_date}&toDate={expire_date}'
    if ticker == 'SPXW':
        ticker = '$SPX.X'
    elif ticker == 'YELP':
        return None
    full_url = endpoint.format(stock_ticker=ticker, contract_type=option_type, expire_date=expire_date)

    page = requests.get(
        url=full_url,
        params={'apikey': td_consumer_key}
    )

    page_content = json.loads(page.content)

    if page_content["status"] == "FAILED":
        print(f'Unable to load option information from TD for: {ticker} {option_type} @{strike_price} {expire_date}')
        return None
    else:
        raw_date_now = date.today()
        date_now = str(raw_date_now.year) + '-' + str(raw_date_now.month) + '-' + str(raw_date_now.day)
        dt_date_now = datetime.datetime.strptime(date_now, '%Y-%m-%d')
        dt_expire_date = datetime.datetime.strptime(expire_date, '%Y-%m-%d')
        dt_days_to_expire = dt_expire_date - dt_date_now
        days_to_expire = dt_days_to_expire.days
        content = page_content['callExpDateMap'][expire_date+f':{days_to_expire}'][strike_price][0]['last']

    print(f'The most recent premium for {ticker} {strike_price} {option_type} is:')

    return content


if __name__ == '__main__':
    ticker = 'APPL'
    option_type = 'CALL'
    strike_price = '132'
    expire_date = '2022-12-27'
    get_asset_info(ticker, option_type, strike_price, expire_date)
