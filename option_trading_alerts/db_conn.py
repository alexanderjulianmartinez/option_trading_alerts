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


def create_table(conn, create_sql_stmt):
    """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_sql_stmt: a CREATE TABLE statement
        :return:
        """
    try:
        c = conn.cursor()
        c.execute(create_sql_stmt)
        print('Table successfully created!')
    except Error as e:
        print(e)


def add_option_alert(conn, option):
    """
    Create a new option alert into the options_alerts table
    :param conn:
    :param option:
    :return: option id
    """
    sql = ''' INSERT INTO options_alerts(ticker, option_type, expire_date, strike_price, trade_premium)
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
        INSERT INTO trades(option_id, ticker, option_type, expire_date, strike_price, trade_premium, curr_premium)
        VALUES(?, ?, ?, ?, ?, ?, ?)
    '''
    cur = conn.cursor()
    cur.execute(sql, trade)
    conn.commit()
    return cur.lastrowid


def main(ticker, option_type, expire_date, strike_price, alert_premium, curr_premium):
    database = r"C:\sqlite\db\pythonsqlite.db"

    sql_create_options_alerts_table = """ CREATE TABLE IF NOT EXISTS options_alerts (
                                              id integer PRIMARY KEY AUTOINCREMENT,
                                              ticker text NOT NULL,
                                              option_type text,
                                              expire_date text,
                                              strike_price text,
                                              alert_premium text,
                                              trade_premium text
                                          ); """

    sql_create_trades_table = """CREATE TABLE IF NOT EXISTS trades (
                                      id integer PRIMARY KEY AUTOINCREMENT,
                                      option_id integer NOT NULL,
                                      ticker text NOT NULL,
                                      option_type text,
                                      expire_date text,
                                      strike_price text,
                                      trade_premium text,
                                      curr_premium text
                                        
                                 );"""

    # create a database connection
    conn = create_conn(database)
    with conn:

        print('Creating options_alerts table...')
        create_table(conn, sql_create_options_alerts_table)

        print('Creating trades table...')
        create_table(conn, sql_create_trades_table)

        option = (ticker, option_type, expire_date, strike_price, curr_premium)
        option_id = add_option_alert(conn, option)
        print(f'Stored Option Alert #{option_id} in option_alerts table')

        trade = (option_id, ticker, option_type, expire_date, strike_price, alert_premium, curr_premium)

        trade_id = create_trade(conn, trade)
        print(f'Stored Trade #{trade_id} in trade table')


if __name__ == '__main__':
    example_ticker = 'AAPL'
    example_option_type = 'CALL'
    example_expire_date = '12-30-2022'
    example_strike_price = '132.0'
    example_alert_premium = '1.98'
    example_curr_premium = example_alert_premium
    main(
        example_ticker,
        example_option_type,
        example_expire_date,
        example_strike_price,
        example_alert_premium,
        example_curr_premium
    )

