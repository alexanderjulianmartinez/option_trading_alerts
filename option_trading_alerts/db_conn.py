import sqlite3
from sqlite3 import Error


def create_conn(db_file):
    """ Create a db connection with SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def add_option_alert(conn, option):
    """
    Create a new option alert into the options_alerts table
    :param conn:
    :param option:
    :return: option id
    """
    sql = ''' INSERT INTO options_alerts(ticker, option_type, alert_expire_date, alert_premium, curr_price)
              VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, option)
    conn.commit()
    return cur.lastrowid


def create_trade(conn, trade):
    """
    Create a new trade into the trades table
    :param conn:
    :param trade:
    :return: trade id
    """
    sql = ''' 
        INSERT INTO trades(option_id, ticker, option_type, expire_date, strike_price, trade_premium)
        VALUES(?, ?, ?, ?, ?, ?)
    '''
    cur = conn.cursor()
    cur.execute(sql, trade)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create a database connection
    conn = create_conn(database)
    with conn:
        ticker = 'AAPL'
        option_type = 'CALL'
        expire_date = '12-30-2022'
        strike_price = '132.0'
        alert_premium = '1.98'
        curr_premium = alert_premium

        option = (ticker, option_type, expire_date, strike_price, alert_premium, curr_premium)
        option_id = add_option_alert(conn, option)

        trade = (option_id, ticker, option_type, expire_date, strike_price, alert_premium, curr_premium)

        create_trade(conn, trade)


if __name__ == '__main__':
    main()
