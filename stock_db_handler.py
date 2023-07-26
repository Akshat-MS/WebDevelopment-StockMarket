import sqlite3
from datetime import datetime
import logging

from logger import Logger

class StockDataManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_stock_data_table()
        self._create_job_table()
        self.last_job_id = self._get_last_job_id()

    def _connect(self):
        try:
            Logger.get_instance().log(logging.INFO,'StockDataManager','_connect()' + self.db_path)
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            Logger.get_instance().log(logging.INFO,'StockDataManager','_connect():Connected to the database successfully...')
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','_connect():An error occurred while connecting to the database: ' + str(e))
            raise e

    def _create_stock_data_table(self):
        Logger.get_instance().log(logging.INFO,'StockDataManager','_create_stock_data_table()')
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS basic_stock_data (
                company TEXT,
                Datetime DATETIME,
                Adj_close REAL,
                high REAL,
                low REAL,
                close REAL,
                open REAL,
                volume INTEGER,
                PRIMARY KEY (company, Datetime)
            )''')
            Logger.get_instance().log(logging.INFO,'StockDataManager','_create_stock_data_table(): Create Table basic_stock_data'
                                      + '\nSchema as : company TEXT, Datetime DATETIME, Adj_close REAL, high REAL, low REAL, close REAL, open REAL, volume INTEGER'
                                      + '\n with Primary Key as company, Datetime')
            
            self.cursor.execute('''CREATE INDEX IF NOT EXISTS idx_company ON basic_stock_data (company)''')
            Logger.get_instance().log(logging.INFO,'StockDataManager','_create_stock_data_table(): basic_stock_data table created successfully...')

        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','_create_stock_data_table(): Error occurred while creating the table: ' + str(e))
            raise e
        
    def insert_stock_data(self, stock_data,stocks):
        try:
            # Insert the fetched stock data into the table
            Logger.get_instance().log(logging.INFO,'StockDataManager','insert_stock_data() : stocks or company name: ' + stocks)
            #Logger.get_instance().log(logging.DEBUG,'StockDataManager','insert_stock_data() : Data as a dataframe: ' + stock_data.to_string())
            symbols = stocks.split()
            for company in symbols:
                Logger.get_instance().log(logging.DEBUG,'StockDataManager','insert_stock_data() : Company Name: ' + company)
                temp_df = stock_data[[('adj_close', company),('high', company),('low', company),('close', company),
                                    ('open', company),('volume', company)]]
                temp_df = temp_df.droplevel(1, axis=1)
                temp_df.reset_index(inplace=True)
                temp_df.insert(0, 'company', company)

                try:
                    # Insert the data into the SQLite table
                    temp_df.to_sql('basic_stock_data', self.conn, if_exists='append', index=False)
                except sqlite3.IntegrityError as e:
                    if str(e) == 'UNIQUE constraint failed: basic_stock_data.company, basic_stock_data.Datetime':
                        # Handle unique constraint violation
                        Logger.get_instance().log(logging.INFO,'StockDataManager','insert_stock_data(): Duplicate record found.')
                    else:
                        # Handle other integrity errors
                        Logger.get_instance().log(logging.CRITICAL,'StockDataManager','insert_stock_data():sqlite3.IntegrityError occurred while inserting the data: '
                                                   + str(e))
                except Exception as e:
                    # Handle other exceptions
                    Logger.get_instance().log(logging.CRITICAL, 'StockDataManager', 'insert_stock_data(): Error occurred while inserting data for company: '
                                               + company + ' - ' + str(e))
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','insert_stock_data():Error occurred while inserting the data: ' + str(e))
            raise e

        except Exception as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','insert_stock_data():Error occurred while inserting the data: ' + str(e))
            raise e

    def _create_job_table(self):
        Logger.get_instance().log(logging.INFO,'StockDataManager','_create_job_table()')
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS job (
                job_id TEXT,
                collection_strt_tm DATETIME,
                successful_fetch_tm DATETIME,
                job_status TEXT,
                num_rec INTEGER,
                PRIMARY KEY (job_id)
            )''')
            Logger.get_instance().log(logging.INFO,'StockDataManager','_create_job_table(): Create Table job'
                                      + '\nSchema as : job_id TEXT, collection_strt_tm DATETIME, successful_fetch_tm DATETIME, job_status TEXT, num_rec INTEGER'
                                      + '\n with Primary Key as job_id')
            Logger.get_instance().log(logging.INFO,'StockDataManager','_create_job_table(): Job Table created successfully...')
            pass
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','_create_job_table(): Error occurred while creating the Job ßtable: ' + str(e))
            raise e
        
    def _get_last_job_id(self):
        try:
            # Connect to the database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get the current maximum job_id from the database
            cursor.execute("SELECT MAX(job_id) FROM job")
            result = cursor.fetchone()
            max_job_id = result[0]

            # Close the database connection
            conn.close()

            if max_job_id is None:
                return 0
            else:
                return int(max_job_id[1:])
        except Exception as e:
            # Handle the exception or log the error
            raise e
    def insert_job_data(self, job_details):
        
        Logger.get_instance().log(logging.INFO, 'StockDataManager', 'insert_job_data():Jobs Details:' + str(job_details))

        # Extract job details
        collection_start_time = job_details['collection_strt_dt']
        successful_fetch_time = job_details['succesful_strt_dt']
        job_status = job_details['job_status']
        num_rec = job_details['rec_cnt']

        new_job_id = None

        try:

            # Generate the new job_id
            self.last_job_id += 1
            new_job_id = 'D' + str(self.last_job_id).zfill(8)

            # Check if the collection_strt_tm is unique
            sql_query = "SELECT COUNT(*) FROM job WHERE collection_strt_tm = ?"
            self.cursor.execute(sql_query, (collection_start_time,))
            count = self.cursor.fetchone()[0]

            if count == 0:

                # Prepare the SQL statement
                sql_query = "INSERT OR IGNORE INTO job (job_id, collection_strt_tm, successful_fetch_tm, job_status, num_rec) VALUES (?, ?, ?, ?, ?)"
                Logger.get_instance().log(logging.DEBUG, 'StockDataManager','insert_job_data(): job_id: ' + new_job_id + ' collection_start_time: ' 
                                        + collection_start_time.strftime("%Y-%m-%d %H:%M:%S%z") + ' successful_fetch_time: ' 
                                        + successful_fetch_time.strftime("%Y-%m-%d %H:%M:%S%z") + ' job_status: ' + job_status + ' num_rec: ' + str(num_rec))

                # Execute the SQL statement with the job details
                self.cursor.execute(sql_query,
                                    (new_job_id, collection_start_time, successful_fetch_time, job_status, num_rec))
                self.conn.commit()
                Logger.get_instance().log(logging.INFO, 'StockDataManager', 'insert_job_data(): Job Data inserted successfully...')
            else:
                # The collection_strt_tm is not unique, so we cannot insert the new data
                Logger.get_instance().log(logging.WARNING, 'StockDataManager', 'insert_job_data(): Collection start time already exists...')

        except Exception as e:
            Logger.get_instance().log(logging.CRITICAL, 'StockDataManager', 'insert_job_data(): Error occurred while inserting job data: ' + str(e) 
                                      + '\nParameters: job_id: ' + new_job_id + ' collection_start_time: ' + collection_start_time.strftime("%Y-%m-%d %H:%M:%S%z") + ' successful_fetch_time: ' 
                                      + successful_fetch_time.strftime("%Y-%m-%d %H:%M:%S%z") + ' job_status: ' + job_status + ' num_rec: ' + str(num_rec))
            raise e

    def fetch_pending_failed_jobs(self):

        try:
            Logger.get_instance().log(logging.INFO, 'StockDataManager', 'fetch_pending_failed_jobs():SELECT query to fetch pending and failed jobs'
                                      + '\nQuery:SELECT * FROM job WHERE job_status = "pending" OR job_status = "failed"')
            # SELECT query to fetch pending and failed jobs.
            self.cursor.execute("SELECT * FROM job WHERE job_status = 'pending' OR job_status = 'failed'")
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','fetch_pending_failed_jobs():An error occurred while fetching Job information: ' + str(e))
            raise e

    def update_job_data(self, job_details):
        
        Logger.get_instance().log(logging.INFO, 'StockDataManager', 'update_job_data(): Job Details: ' + str(job_details))

        # Extract job details
        job_id = job_details['job_id']
        collection_start_time = job_details['collection_strt_dt']
        successful_fetch_time = job_details['succesful_strt_dt']
        job_status = job_details['job_status']
        num_rec = job_details['rec_cnt']

        try:

            # Prepare the SQL statement
            sql_query = "UPDATE job SET collection_strt_tm = ?, successful_fetch_tm = ?, job_status = ?, num_rec = ? WHERE job_id = ?"

            Logger.get_instance().log(logging.DEBUG, 'StockDataManager', 'update_job_data(): job_id: ' + job_id + ' collection_start_time: '
                                    + collection_start_time + ' successful_fetch_time: ' + successful_fetch_time + ' job_status: '
                                    + job_status + ' num_rec: ' + str(num_rec))

            # Execute the SQL statement with the job details
            self.cursor.execute(sql_query, (collection_start_time, successful_fetch_time, job_status, num_rec, job_id))
            self.conn.commit()

            Logger.get_instance().log(logging.INFO, 'StockDataManager', 'update_job_data(): Job Data updated successfully...')
        except Exception as e:
            Logger.get_instance().log(logging.CRITICAL, 'StockDataManager', 'update_job_data(): Error occurred while updating job data: ' + str(e)
                                    + '\nParameters: job_id: ' + job_id + ' collection_start_time: ' + collection_start_time
                                    + ' successful_fetch_time: ' + successful_fetch_time.strftime("%Y-%m-%d %H:%M:%S")  + ' job_status: ' + job_status
                                    + ' num_rec: ' + str(num_rec))
            raise e

    def fetch_data(self):
        try:
            Logger.get_instance().log(logging.INFO,'StockDataManager','fetch_data() : SELECT all data from the basic_stock_data table' 
                                + 'Query:SELECT * FROM basic_stock_data')
            self.cursor.execute("SELECT * FROM basic_stock_data")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','fetch_data():An error occurred while fetching the data: ' + str(e))
            raise e
        
    def generate_search_query(self,start_date=None, end_date=None, company=None,limit=None, offset=None):
        query = "SELECT * FROM basic_stock_data"
        conditions = []

        if start_date:
            conditions.append(f"DATE(Datetime) >= '{start_date}'")
        
        if end_date:
            conditions.append(f"DATE(Datetime) <= '{end_date}'")

        if company:
            conditions.append(f"company = '{company}'")
        
        print('Conditions',conditions)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        print('Query :- ', query)

        if limit:
            query += f" LIMIT {limit}"
        
        if offset:
            query += f" OFFSET {offset}"

        return query
    
    def fetch_data_api(self,req_param):
        try:

            company = req_param.get('company')
            start_date = req_param.get('startdate')
            end_date = req_param.get('enddate')
            limit = req_param.get('limit',500)
            offset = req_param.get('offset',0)

            Logger.get_instance().log(logging.INFO,'StockDataManager','fetch_data_by_company_and_dates() : Input Parameters are : ' 
                                  + '\nCompany Name:' + company + '\nStart Date:' + str(start_date) 
                                  + '\nEnd Date:' + str(end_date) + '\nLimit:' + str(limit) + '\nOffset:' + str(offset))
            
            
            query = self.generate_search_query(start_date, end_date, company,limit, offset)
            print("Final Query :- ", query)
            self.cursor.execute(query)
            '''self.cursor.execute(
                "SELECT * FROM basic_stock_data WHERE company = ? AND Datetime BETWEEN ? AND ? LIMIT ? OFFSET ?",
                (company, start_date, end_date,limit, offset)
            )'''

            rows = self.cursor.fetchall()

            columns = [column[0] for column in self.cursor.description]
            return rows ,columns
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','fetch_data():An error occurred while fetching the data: ' + str(e))
            raise e
            
    def fetch_data_by_company_and_dates(self, company, start_date, end_date):

        Logger.get_instance().log(logging.INFO,'StockDataManager','fetch_data_by_company_and_dates() : Input Parameters are : ' 
                                  + '\nCompany Name:' + company + '\nStart Date:' + str(start_date) 
                                  + '\nEnd Date:' + str(end_date))

        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S%z")
        start_date_str = start_date_str[:-2] + ":" + start_date_str[-2:]

        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S%z")
        end_date_str = end_date_str[:-2] + ":" + end_date_str[-2:]
        
        try:
            Logger.get_instance().log(logging.INFO,'StockDataManager','fetch_data_by_company_and_dates() : SELECT data based on company name and between dates from the basic_stock_data table' 
                                + 'SELECT * FROM basic_stock_data WHERE company = ' + company + ' AND Datetime BETWEEN ' +start_date_str + ' AND ' + end_date_str)
            self.cursor.execute(
                "SELECT * FROM basic_stock_data WHERE company = ? AND Datetime BETWEEN ? AND ?",
                (company, start_date_str,end_date_str)
            )
            
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','fetch_data_by_company_and_dates():Error occurred while fetching the data based on company and time : ' 
                                      + str(e))
            raise e

    def fetch_companies(self):
        try:
            self.cursor.execute("SELECT DISTINCT company FROM basic_stock_data")
            rows = self.cursor.fetchall()
            Logger.get_instance().log(logging.INFO,'StockDataManager','fetch_companies():Fetched the companies: ' + str(rows))
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','fetch_companies():Error occurred while fetching the companies: ' + str(e))
            raise e


    def disconnect(self):
        try:
            self.conn.close()
            Logger.get_instance().log(logging.INFO,'StockDataManager','disconnect() :Disconnected from the database.')
        except sqlite3.Error as e:
            Logger.get_instance().log(logging.CRITICAL,'StockDataManager','disconnect():Error occurred while disconnecting from the database: ' + str(e))
            raise e


def main():

    '''db_path = '/Volumes/Development/_GitHub/StockMarket-Data/database/stock_data.db'

    stock_manager = StockDataManager(db_path)

    fetched_data = stock_manager.fetch_data()
    if fetched_data:
        for row in fetched_data:
            print(row)

    company = 'Company A'
    start_date = '2023-06-15 09:00:00'
    end_date = '2023-06-16 09:00:00'
    fetched_data = stock_manager.fetch_data_by_company_and_dates(company, start_date, end_date)
    if fetched_data:
        for row in fetched_data:
            print(row)

    stock_manager.disconnect()'''
    pass

if __name__ == '__main__':
    main()

