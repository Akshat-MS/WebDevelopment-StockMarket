import pytz
from datetime import datetime

from config_reader import ConfigReader 

class TimeUtil:
    
    def __init__(self):
        
        self.config_file_path = './config_files/config.ini'
        self.reader = ConfigReader(self.config_file_path)
        self.reader.read_config()

        # Timezone
        self.timezone_offset_str = self.reader.get_timezone()


    def get_loacal_time(self,date_time):       

        # Localize the start date and time to the specified timezone
        # Parse timezone offset string and create timezone object.
        timezone_offset_hours, timezone_offset_minutes = map(int, self.timezone_offset_str.split(':'))
        timezone = pytz.FixedOffset(timezone_offset_hours * 60 + timezone_offset_minutes)

        # Localize the date and time to the specified timezone
        l_date_time = timezone.localize(date_time)

        return l_date_time
    
if __name__ == '__main__':
    pass