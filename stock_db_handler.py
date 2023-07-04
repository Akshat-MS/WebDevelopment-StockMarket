import sqlite3
from datetime import datetime

class StockDataManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_table()

    def _connect(self):
        try:
            print("DEBUG:STOCK_DB_HANDLER:_connect():Database Path - ",self.db_path)
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("DEBUG:STOCK_DB_HANDLER:_connect():Connected to the database successfully...")
        except sqlite3.Error as e:
            print("An error occurred while connecting to the database:", e)

    def _create_table(self):
        print("DEBUG:STOCK_DB_HANDLER:_create_table()")
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS basic_stock_data (
                company TEXT,
                Datetime DATETIME,
                Adj_close REAL,
                high REAL,
                low REAL,
                close REAL,
                open REAL,
                volume INTEGER,
                PRIMARY KEY (company, Datetime)
            )''')
            self.cursor.execute('''CREATE INDEX IF NOT EXISTS idx_company ON basic_stock_data (company)''')
            print("DEBUG:STOCK_DB_HANDLER:_create_table:Table 'basic_stock_data' created with index on 'company'.")
        except sqlite3.Error as e:
            print("ERROR:STOCK_DB_HANDLER:_create_table:An error occurred while creating the table: ", e)

    def insert_data(self, stock_data,stocks):
        try:
            # Insert the fetched stock data into the table
            #print(stocks)
            symbols = stocks.split()
            for company in symbols:
                #print(company)
                
                temp_df = stock_data[[('adj_close', company),('high', company),('low', company),('close', company),
                                    ('open', company),('volume', company)]]
                temp_df = temp_df.droplevel(1, axis=1)
                temp_df.reset_index(inplace=True)
                temp_df.insert(0, 'company', company)

                #print(temp_df.columns)

                # Insert the data into the SQLite table
                temp_df.to_sql('basic_stock_data', self.conn, if_exists='append', index=False)

        except sqlite3.Error as e:
            print("An error occurred while inserting the data:", e)

    def fetch_data(self):
        try:
            self.cursor.execute("SELECT * FROM basic_stock_data")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print("An error occurred while fetching the data:", e)
            
    def fetch_data_by_company_and_dates(self, company, start_date, end_date):

        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S%z")
        start_date_str = start_date_str[:-2] + ":" + start_date_str[-2:]

        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S%z")
        end_date_str = end_date_str[:-2] + ":" + end_date_str[-2:]        
        
        print("Start Datetime and End Datetime",start_date,end_date)
        print(type(start_date_str),type(end_date_str))
        print("Test time valueeeeeeeeeeeeee ",start_date_str,end_date_str)
        
        try:
            self.cursor.execute(
                "SELECT * FROM basic_stock_data WHERE company = ? AND Datetime BETWEEN ? AND ?",
                (company, start_date_str,end_date_str)
            )
            
            rows = self.cursor.fetchall()
            print(rows)
            return rows
        except sqlite3.Error as e:
            print("An error occurred while fetching the data:", e)

    def fetch_companies(self):
        try:
            self.cursor.execute("SELECT DISTINCT company FROM basic_stock_data")
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            print("An error occurred while fetching distinct companies:", e)


    def disconnect(self):
        try:
            self.conn.close()
            print("Disconnected from the database.")
        except sqlite3.Error as e:
            print("An error occurred while disconnecting from the database:", e)


def main():

    '''db_path = '/Volumes/Development/_GitHub/StockMarket-Data/database/stock_data.db'

    stock_manager = StockDataManager(db_path)

    fetched_data = stock_manager.fetch_data()
    if fetched_data:
        for row in fetched_data:
            print(row)

    company = 'Company A'
    start_date = '2023-06-15 09:00:00'
    end_date = '2023-06-16 09:00:00'
    fetched_data = stock_manager.fetch_data_by_company_and_dates(company, start_date, end_date)
    if fetched_data:
        for row in fetched_data:
            print(row)

    stock_manager.disconnect()'''
    pass

if __name__ == '__main__':
    main()

