import yfinance as yf
from datetime import datetime, time
import logging

from stock_db_handler import StockDataManager
from config_reader import ConfigReader
from time_util import TimeUtil
from logger import Logger

class StockDataRegularCollector:
    def __init__(self):
        self.time_util = TimeUtil()
        self.job_info = []

    def fetch_daily_stock_data(self):

        reader = ConfigReader()
        reader.read_config()

        try:

            reader = ConfigReader()
            reader.read_config()
            db_path = reader.get_db_path()
            stk_db_handler = StockDataManager(db_path)

            stocks = reader.get_stocks()
            job_data = stk_db_handler.fetch_pending_failed_jobs()
            stk_db_handler.disconnect()

            if job_data is not None:
                for self.job_info  in job_data:
                    Logger.get_instance().log(logging.INFO,'StockDataRegularCollector','fetch_daily_stock_data():job_data: ' + str(self.job_info ))
                
                    # Fetch current date and time
                    current_datetime = datetime.now()

                    # Retrieve interval value from the config.ini
                    interval = reader.get_collection_interval()

                    start_date_time = self.job_info [1]
                    # Convert the start date string to a datetime format
                    start_datetm = datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S")
                    l_start_date_time = self.time_util.get_loacal_time(start_datetm)

                    # Set the desired end time
                    end_time = time(15, 30, 0)
                    # Combine current date with end time
                    end_datetime = datetime.combine(start_datetm.date(), end_time)
                    
                    # Localize end datetime to the specified timezone
                    # Localize start datetime & end datetime to the specified timezone
                    # l_start_date_time = self.time_util.get_loacal_time(start_datetime)
                    l_end_date_time = self.time_util.get_loacal_time(end_datetime)

                    stock_data = yf.download(stocks,start = l_start_date_time,end = l_end_date_time,interval = interval)

                    if stock_data is not None:
                        stock_data.rename(columns = {'Adj Close':'adj_close', 'Close':'close','High':'high', 'Low':'low','Open':'open', 'Volume':'volume'}, inplace = True)
                        if self._write_data_to_database(stock_data,stocks,db_path) == True :
                            no_records = stock_data.shape[0] * len(stocks.split(" "))
                            self._update_job_status('done',no_records)
                        else:
                            self._update_job_status('failed',0)
                    else:
                        Logger.get_instance().log(logging.ERROR,'StockDataRegularCollector','fetch_daily_stock_data():Error occurred while fetching stock data: ' + str(e))
                        self._update_job_status('failed',0)

                    # return stock_data

        except Exception as e:
            Logger.get_instance().log(logging.ERROR,'StockDataRegularCollector','fetch_daily_stock_data():Error occurred while fetching stock data: ' + str(e))
            raise e
    
    
    def _write_data_to_database(self, stk_data,symbols, db_path):
        try:
            stk_db_handler = StockDataManager(db_path)
            stk_db_handler.insert_stock_data(stk_data,symbols)
            stk_db_handler.disconnect()
            Logger.get_instance().log(logging.INFO,'StockDataRegularCollector','_write_data_to_database : Data stored successfully')
            return True
        except Exception as e:
            Logger.get_instance().log(logging.ERROR,'StockDataRegularCollector','_write_data_to_database : Error occurred while storing stock data : ' + str(e))
            return False

    def _update_job_status(self,job_status,num_rec):

        job_details ={}

        try:
            reader = ConfigReader()
            reader.read_config()
            db_path = reader.get_db_path()
            stk_db_handler = StockDataManager(db_path)

            # Current Date amd time.
            current_datetime = datetime.now()
            # Formatted date and time object in a specific format (input type is datetime object and output type is datetime object)
            formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            job_details["job_id"] = self.job_info[0]
            job_details["collection_strt_dt"] = self.job_info[1]
            job_details["succesful_strt_dt"] = formatted_time
            job_details["job_status"] = job_status
            job_details["rec_cnt"] = num_rec

            Logger.get_instance().log(logging.INFO,'StockDataRegularCollector','schedule_job:Paramters: ' + str(job_details))

            stk_db_handler.update_job_data(job_details)
            stk_db_handler.disconnect()
            
        except Exception as e:
            Logger.get_instance().log(logging.ERROR,'StockDataRegularCollector','schedule_job:Error occurred while scheduling job: ' + str(e))

if __name__ == '__main__':
    test = StockDataRegularCollector()
    test.fetch_daily_stock_data()
    pass