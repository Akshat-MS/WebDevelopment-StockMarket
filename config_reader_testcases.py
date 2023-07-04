import unittest
import configparser
from config_reader import ConfigReader

class ConfigReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.config_file_path = './config_files/config.ini'
        self.reader = ConfigReader(self.config_file_path)
        self.reader.read_config()

    def test_get_stocks(self):
        expected_stocks = 'RELIANCE.NS TCS.NS HDFCBANK.NS INFY.NS ICICIBANK.NS HINDUNILVR.NS SBIN.NS KOTAKBANK.NS ASIANPAINT.NS AXISBANK.NS LT.NS MARUTI.NS HCLTECH.NS IOC.NS BPCL.NS NTPC.NS POWERGRID.NS ONGC.NS WIPRO.NS COALINDIA.NS SUNPHARMA.NS INDUSINDBK.NS CIPLA.NS ULTRACEMCO.NS HEROMOTOCO.NS'
        #'SBIN.NS RELIANCE.NS ICICIBANK.NS TCS.NS'
        actual_stocks = self.reader.get_stocks()
        print(actual_stocks)
        self.assertEqual(actual_stocks, expected_stocks)

    def test_get_timezone(self):
        expected_timezone = '5:30'
        actual_timezone = self.reader.get_timezone()
        self.assertEqual(actual_timezone, expected_timezone)

    def test_get_interval(self):
        expected_interval = '1m'
        actual_interval = self.reader.get_collection_interval()
        self.assertEqual(actual_interval, expected_interval)

    def test_get_start_time(self):
        expected_start_time = '2023-06-27 09:00:00'
        actual_start_time = self.reader.get_start_date_time()
        self.assertEqual(actual_start_time, expected_start_time)

    def test_get_end_time(self):
        expected_end_time = '2023-06-27 16:00:00'
        actual_end_time = self.reader.get_end_date_time()
        self.assertEqual(actual_end_time, expected_end_time)

    def test_get_db_path(self):
        expected_db_path = "./database/stock_data.db"
        actual_db_path = self.reader.get_db_path()
        self.assertEqual(actual_db_path, expected_db_path)

    def test_invalid_section(self):
        with self.assertRaises(configparser.NoSectionError):
            self.reader.config.get('invalid_section', 'invalid_option')

    def test_missing_option(self):
        with self.assertRaises(configparser.NoOptionError):
            self.reader.config.get('stocks', 'invalid_option')

    @classmethod
    def setUpClass(cls):
        cls.suite = unittest.TestLoader().loadTestsFromTestCase(ConfigReaderTestCase)

    @classmethod
    def run_tests(cls):
        runner = unittest.TextTestRunner()
        result = runner.run(cls.suite)
        return result

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConfigReaderTestCase)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    test_count = result.testsRun
    test_passed = test_count - len(result.errors) - len(result.failures)

    print(f"Total Tests Run: {test_count}")
    print(f"Tests Passed: {test_passed}")
    print(f"Tests Failed: {len(result.errors) + len(result.failures)}")
