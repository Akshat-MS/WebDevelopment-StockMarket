import yfinance as yf
from datetime import datetime, time, timedelta
from config_reader import ConfigReader
from stock_db_handler import StockDataManager
from time_util import TimeUtil

class StockDataHistoryCollector:
    def __init__(self) -> None:
        self.time_util = TimeUtil()
        self.list_strt_end_interval = []
        pass    

    def _create_list_history_collection(self):

        # Fetch current date and time
        current_datetime = datetime.now()
        # Set the desired start time
        start_time = time(9, 15, 0)
        # Set the desired end time
        end_time = time(15, 30, 0)

        intervals = [
            (1, 7, '1m'),
            (8, 14 ,'1m'),
            (15, 21, '1m'),
            (22, 28, '1m'),
            (29, 59, '2m'),
            (60, 729, '1h')
        ]

        for start_days, end_days, interval in intervals:

            # Combine current date with start and end times
            end_datetime = datetime.combine(current_datetime.date() - timedelta(days=start_days), start_time)
            start_datetime = datetime.combine(current_datetime.date() - timedelta(days=end_days), end_time)

            # Append to the list
            self.list_strt_end_interval.append([start_datetime, end_datetime, interval])

    def _write_data_to_database(self, stk_data,symbols, db_path):
        try:
            stk_db_handler = StockDataManager(db_path)
            stk_db_handler.insert_data(stk_data,symbols)
            stk_db_handler.disconnect()
            print("Data stored successfully")
        except Exception as e:
            print("Error occurred while storing stock data:", str(e))

    def fetch_history_data(self):

        self._create_list_history_collection()

        config_file_path = './config_files/config.ini'
        reader = ConfigReader(config_file_path)
        reader.read_config()

        try:

            for item in self.list_strt_end_interval:

                # Localize start datetime & end datetime to the specified timezone
                l_start_date_time = self.time_util.get_loacal_time(item[0])
                l_end_date_time = self.time_util.get_loacal_time(item[1])

                stk_data = yf.download(reader.get_stocks(), start=l_start_date_time, end=l_end_date_time, interval=item[2])
                stk_data.rename(columns={'Adj Close':'adj_close', 'Close':'close', 'High':'high', 'Low':'low', 'Open':'open', 'Volume':'volume'}, inplace=True)

                if stk_data is not None:
                    db_path = reader.get_db_path()
                    self._write_data_to_database(stk_data, reader.get_stocks(),db_path)
                else:
                    print("No Data available for this interval", l_start_date_time, l_end_date_time)
        
        except Exception as e:
            print("Error occurred while fetching stock data:", str(e))
            return None

if __name__ == '__main__':
    stock_data_collector = StockDataHistoryCollector()
    stock_data_collector.fetch_history_data()
