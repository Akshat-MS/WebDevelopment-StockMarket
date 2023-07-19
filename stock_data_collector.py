import yfinance as yf

from datetime import datetime,time

from config_reader import ConfigReader 
from stock_db_handler import StockDataManager
from time_util import TimeUtil

class StockDataCollector:
    def __init__(self):
        self.time_util = TimeUtil()

    def fetch_data(self):
        reader = ConfigReader()
        reader.read_config()

        try:

            # Get localized Start Time
            start_date_time_str = reader.get_start_date_time()
            start_date_time = datetime.strptime(start_date_time_str, "%Y-%m-%d %H:%M:%S")

            print("Start Date", start_date_time)
            l_start_date_time = self.time_util.get_loacal_time(start_date_time)

            # Get localized End Time
            end_date_time_str = reader.get_end_date_time()
            end_date_time = datetime.strptime(end_date_time_str, "%Y-%m-%d %H:%M:%S")
            l_end_date_time = self.time_util.get_loacal_time(end_date_time)

            return self.fetch_history_stock_data(reader.get_stocks(),l_start_date_time,l_end_date_time,reader.get_collection_interval())
        
        except Exception as e:
            print("Error occurred while fetching stock data:", str(e))
            return None

    
    def fetch_history_stock_data(self,stocks,start_time,end_time,interval):
        try:
            stock_data = yf.download(stocks,start = start_time,end = end_time,interval = interval)
            stock_data.rename(columns = {'Adj Close':'adj_close', 'Close':'close','High':'high', 'Low':'low','Open':'open', 'Volume':'volume'}, inplace = True)
            return stock_data
        except Exception as e:
            print("Error occurred while fetching stock data:", str(e))
            return None
        
    def fetch_daily_stock_data(self,stocks):

        reader = ConfigReader()
        reader.read_config()

        try:
            # Fetch current date and time
            current_datetime = datetime.now()
            
            # Retrieve interval value from the config.ini
            interval = reader.get_collection_interval()

            # Set the desired start time
            start_time = time(9, 15, 0)
            # Combine current date with start time
            start_datetime = datetime.combine(current_datetime.date(), start_time)

            # Set the desired end time
            end_time = time(15, 30, 0)
            # Combine current date with end time
            end_datetime = datetime.combine(current_datetime.date(), end_time)
            # Localize end datetime to the specified timezone

            # Localize start datetime & end datetime to the specified timezone
            l_start_date_time = self.time_util.get_loacal_time(start_datetime)
            l_end_date_time = self.time_util.get_loacal_time(end_datetime)

            stock_data = yf.download(stocks,start = l_start_date_time,end = l_end_date_time,interval = interval)
            stock_data.rename(columns = {'Adj Close':'adj_close', 'Close':'close','High':'high', 'Low':'low','Open':'open', 'Volume':'volume'}, inplace = True)

            return stock_data

        except Exception as e:
            print("Error occurred while fetching stock data:", str(e))
            return None
    
    def store_data_db(self,stock_data):

        reader = ConfigReader()
        reader.read_config()

        db_path = reader.get_db_path()
        stk_db_handler = StockDataManager(db_path)

        stk_db_handler.insert_stock_data(stock_data,reader.get_stocks())

        stk_db_handler.disconnect()

    
def main():
    fetcher = StockDataCollector()
    stk_hist_data = fetcher.fetch_data()
    

    if stk_hist_data is not None:
        fetcher.store_data_db(stk_hist_data)
        #print(stk_hist_data.head())
    else:
        print("No Data")

    
    reader1 = ConfigReader(

    )
    reader1.read_config()

    stk_daily_data = fetcher.fetch_daily_stock_data(reader1.get_stocks())
    
    if stk_daily_data is not None:
        fetcher.store_data_db(stk_daily_data)
        #print(stk_daily_data.head())
    else:
        print("No Data")

if __name__ == '__main__':
    main()
