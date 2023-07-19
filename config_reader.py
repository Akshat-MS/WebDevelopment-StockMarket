import logging
import configparser

from logger import Logger

class ConfigReader :
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.file_path = "./config_files/config.ini"
        
    def read_config(self):
        try :
            Logger.get_instance().log(logging.DEBUG,'ConfigReader','read_config : Read Config file located at :' + self.file_path)
            self.config.read(self.file_path)
        except configparser.Error as e:
            Logger.get_instance().log(logging.ERROR,'ConfigReader','read_config : Error in reading config file : ' + str(e)
                                      + "\nFile Path : " + self.file_path)
            raise e
    
    def get_stocks(self):
        try:
            stocks = self.config.get("stocks","name")
            Logger.get_instance().log(logging.DEBUG,'ConfigReader','get_stocks : Companies name from config file:' + stocks)
            return stocks
        except (configparser.NoOptionError,configparser.NoSectionError) as e:
            Logger.get_instance().log(logging.ERROR,'ConfigReader','get_stocks : No section or Option is available in the config file for stocks :' + str(e)
                                      + "\nSection name: stocks" +  "\nOption name: name")
            raise e
            
    def get_timezone(self):
        try:
            timezone = self.config.get("collection","timezone")
            Logger.get_instance().log(logging.DEBUG,'ConfigReader','get_timezone : Timezone value from config file:' + timezone)
            return timezone
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            Logger.get_instance().log(logging.ERROR,'ConfigReader','get_timezone : No section or Option is available in the config file for timezone' + str(e)
                                      + "\nSection name: collection Or" +  "\nOption name: timezone")
            raise e
            
    def get_start_date_time(self):
        try:
            start_date_time = self.config.get("collection","start_date_time")
            Logger.get_instance().log(logging.DEBUG,'ConfigReader','get_start_date_time : Start Date and Time from config file:' + start_date_time)
            return start_date_time
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            Logger.get_instance().log(logging.ERROR,'ConfigReader','get_start_date_time : No section or Option is available in the config file for start time' + str(e)
                                      + "\nSection name: collection Or" +  "\nOption name: start_date_time")
            raise e
            
    def get_end_date_time(self):
        try:
            end_date_time = self.config.get("collection","end_date_time")
            Logger.get_instance().log(logging.DEBUG,'ConfigReader','get_end_date_time : End Date and Time from config file:' + end_date_time)
            return end_date_time
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            Logger.get_instance().log(logging.ERROR,'ConfigReader','get_end_date_time : No section or Option is available in the config file for end time' + str(e)
                                      + "\nSection name: collection Or" +  "\nOption name: end_date_time")
            raise e
            
    def get_collection_interval(self):
        try:
            collection_interval = self.config.get("collection","interval")
            Logger.get_instance().log(logging.DEBUG,'ConfigReader','get_collection_interval : Collection Interval from config file:' + collection_interval)
            return collection_interval
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            Logger.get_instance().log(logging.ERROR,'ConfigReader','get_collection_interval : No section or Option is available in the config file for collection interval' + str(e)
                                      + "\nSection name: collection Or" +  "\nOption name: interval")
            raise e
            
    def get_db_path(self):
        try:
            db_path = self.config.get("database","db_path")
            Logger.get_instance().log(logging.DEBUG,'ConfigReader','get_db_path : Database Path from config file:' + db_path)
            return db_path
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            Logger.get_instance().log(logging.ERROR,'ConfigReader','get_db_path : No section or Option is available in the config file for database path' + str(e)
                                      + "\nSection name: database Or" +  "\nOption name: db_path")
            raise e

            
def main():
    reader = ConfigReader()
    
    reader.read_config()
    print(reader.get_stocks())
    print(reader.get_timezone())
    print(reader.get_start_date_time())
    print(reader.get_end_date_time())
    print(reader.get_collection_interval())
    print(reader.get_db_path())
    
if __name__ == '__main__':
    main()

        