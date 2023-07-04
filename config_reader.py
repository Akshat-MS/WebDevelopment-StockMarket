import configparser

class ConfigReader :
    def __init__(self,file_path):
        self.config = configparser.ConfigParser()
        self.file_path = file_path
        
    def read_config(self):
        try :
            self.config.read(self.file_path)
            print("DEBUG:CONFIG SETTING:Config File Path - ",self.file_path)
        except configparser.Error as e:
            print("\n Error in read the config file: {e}")
    
    def get_stocks(self):
        try:
            stocks = self.config.get("stocks","name")
            print("DEBUG:CONFIG SETTING:Company Names - ", stocks)
            return stocks
        except (configparser.NoOptionError,configparser.NoSectionError) as e:
            print({"\n No Section or No option is avaliable in the Config File for stocks"})
            
    def get_timezone(self):
        try:
            timezone = self.config.get("collection","timezone")
            print("DEBUG:CONFIG SETTING:Timezone Details - ", timezone)
            return timezone
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            print("\n No section or Option is available in the config file for timezone")
            raise e
            
    def get_start_date_time(self):
        try:
            start_date_time = self.config.get("collection","start_date_time")
            print("DEBUG:CONFIG SETTING:Start Date and Time - ", start_date_time)
            return start_date_time
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            print("\n No section or Option is available in the config file for start time")
            
    def get_end_date_time(self):
        try:
            end_date_time = self.config.get("collection","end_date_time")
            print("DEBUG:CONFIG SETTING:End Date and Time - ", end_date_time)
            return end_date_time
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            print("\n No section or Option is available in the config file for end time")
            
    def get_collection_interval(self):
        try:
            collection_interval = self.config.get("collection","interval")
            print("DEBUG:CONFIG SETTING:Collection Interval - ", collection_interval)
            return collection_interval
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            print("\n No section or Option is available in the config file for collection intrval")
            
    def get_db_path(self):
        try:
            db_path = self.config.get("database","db_path")
            print("DEBUG:CONFIG SETTING:Database Path - ", db_path)
            return db_path
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            print("\n No section or Option is available in the config file for database path")
            
def main():
    config_path = "./config_files/config.ini"
    reader = ConfigReader(config_path)
    
    reader.read_config()
    print(reader.get_stocks())
    print(reader.get_timezone())
    print(reader.get_start_date_time())
    print(reader.get_end_date_time())
    print(reader.get_collection_interval())
    print(reader.get_db_path())
    
if __name__ == '__main__':
    main()

        