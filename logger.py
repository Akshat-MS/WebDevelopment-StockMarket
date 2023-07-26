import logging
import datetime

from logging.handlers import RotatingFileHandler
import configparser

class Logger:

    _instance = None

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance
    
    def __init__(self) -> None:

        self.config = configparser.ConfigParser()
        self.file_path = "./config_files/logging.ini"

        self.config.read(self.file_path)

        log_max_file_size = 1048576
        log_level = logging.INFO
        log_rollover_count = 5

        try:
            log_max_file_size = self.config.get("logging","max_file_size")
        except:
            pass

        try:
            log_level = self.config.get("logging","level")
        except:
            pass

        try:
            log_rollover_count = self.config.get("logging","rollover_count")
            print(type(log_rollover_count),log_rollover_count)
        except:
            pass

        current_time = datetime.datetime.now()

        self.logger = logging.getLogger(__name__)
        max_bytes = int(log_max_file_size)  # Convert max size to integer
        self.logger.setLevel(log_level)

        file_handler = RotatingFileHandler(filename=f'./logs/debug.log', maxBytes=max_bytes, backupCount=5)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s [%(module)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self,level,module,msg):
        log_message = f"[{module}] {msg}"
        self.logger.log(level, log_message)

if __name__ == "__main__":

    #logger = Logger.get_instance()
    #logger.log(logging.DEBUG, 'my_module', 'This is an info message')

    pass
