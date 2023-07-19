import pytz
import logging

from config_reader import ConfigReader 
from logger import Logger

class TimeUtil:
    
    def __init__(self):
        self.reader = ConfigReader()
        self.reader.read_config()

        # Timezone
        self.timezone_offset_str = self.reader.get_timezone()


    def get_loacal_time(self,date_time): 

        Logger.get_instance().log(logging.INFO,'StockDataHistoryCollector','get_loacal_time ' + str(date_time))      

        # Localize the start date and time to the specified timezone
        # Parse timezone offset string and create timezone object.
        timezone_offset_hours, timezone_offset_minutes = map(int, self.timezone_offset_str.split(':'))
        timezone = pytz.FixedOffset(timezone_offset_hours * 60 + timezone_offset_minutes)

        # Localize the date and time to the specified timezone
        l_date_time = timezone.localize(date_time)

        Logger.get_instance().log(logging.DEBUG,'StockDataHistoryCollector','get_loacal_time - Localize Time ' + str(l_date_time))   

        return l_date_time
    
if __name__ == '__main__':
    pass