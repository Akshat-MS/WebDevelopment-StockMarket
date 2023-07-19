from datetime import datetime,time
import logging

from stock_db_handler import StockDataManager
from config_reader import ConfigReader
from logger import Logger

class StockDataJobLogger:
    def __init__(self):
        pass

    def schedule_job(self):

        job_details ={}

        try:
            reader = ConfigReader()
            reader.read_config()
            db_path = reader.get_db_path()
            stk_db_handler = StockDataManager(db_path)

            current_datetime = datetime.now()
            # Set the desired start time
            start_time = time(9, 15, 0)

            job_details['job_id'] = 'D0000001'            
            job_details["collection_strt_dt"] = datetime.combine(current_datetime.date(), start_time)
            job_details["succesful_strt_dt"] = datetime.min
            job_details["job_status"] = 'pending'
            job_details["rec_cnt"] = 0

            Logger.get_instance().log(logging.INFO,'StockDataJobLogger','schedule_job:Paramters: ' + str(job_details))

            stk_db_handler.insert_job_data(job_details)
            stk_db_handler.disconnect()
            
        except Exception as e:
            Logger.get_instance().log(logging.ERROR,'StockDataJobLogger','schedule_job:Error occurred while scheduling job: ' + str(e))

if __name__ =='__main__':
    test = StockDataJobLogger()
    test.schedule_job()
    pass