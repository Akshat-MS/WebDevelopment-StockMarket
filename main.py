from flask import Flask, render_template, request
from datetime import datetime,time,date

from config_reader import ConfigReader 
from stock_db_handler import StockDataManager
from time_util import TimeUtil

def extract_company_name(stock):
    return stock.split(" ")

def is_company_available(company):
    # Return True if the company is available, False otherwise
    symbols = get_company_names()
    return company in symbols

def get_company_names():
    config_file_path = './config_files/config.ini'
    reader = ConfigReader(config_file_path)
    reader.read_config()

    db_path = reader.get_db_path()
    stk_db_handler = StockDataManager(db_path)

    return stk_db_handler.fetch_companies()

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def display_table():

    if request.method == 'POST':

        # Validate the incoming data - range - format etc.
        # Get the selected company from the form submission
        company = request.form.get('company')
        start_date = request.form.get('start-date')
        end_date = request.form.get('end-date')

        # Validate the incoming data
        errors = []

        # Validate start date
        try:
            start_datetm = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid start date format. Please use YYYY-MM-DD.")

        # Validate end date
        try:
            end_datetm = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid end date format. Please use YYYY-MM-DD.")

        # Check if start date is before end date
        if start_datetm and end_datetm and start_datetm > end_datetm:
            errors.append("Start date cannot be after end date.")

        # Check if the selected company is available in the database
        if not is_company_available(company):
            errors.append("Provided company data is not available in the database. Check the company name.")

        # If there are any validation errors, render the template with the error messages
        if errors:
            symbols = get_company_names()  # Replace with your logic to fetch company symbols
            current_date = date.today().isoformat()
            return render_template('index.html', errors=errors, stocks=symbols, current_date=current_date)
        else:

            time_util = TimeUtil()

            config_file_path = './config_files/config.ini'
            reader = ConfigReader(config_file_path)
            reader.read_config()

            db_path = reader.get_db_path()
            stk_db_handler = StockDataManager(db_path)

            # Convert the start date string to a datetime format
            start_datetm = datetime.strptime(start_date, "%Y-%m-%d")
            # Set the desired start time
            start_time = time(9, 15, 0)
            # Combine current date with start time
            start_datetime = datetime.combine(start_datetm, start_time)
            l_start_date_time = time_util.get_loacal_time(start_datetime)

            
            # End Date string to Date fromat.
            end_datetm = datetime.strptime(end_date, "%Y-%m-%d")
            # Set the desired end time
            end_time = time(15, 30, 0)
            # Combine current date with end time
            end_datetime = datetime.combine(end_datetm, end_time)
            l_end_date_time = time_util.get_loacal_time(end_datetime)

            print("POST Selected Start time",l_start_date_time)
            print("POST Selected End Time",l_end_date_time)

            print("POST Selected company:", company)
            print("POST Request - form data:", request.form)

            if company:
                # Fetch data from the database based on the selected company and date range
                data = stk_db_handler.fetch_data_by_company_and_dates(company, l_start_date_time, l_end_date_time)

            symbols = stk_db_handler.fetch_companies()
            stk_db_handler.disconnect()

            # Get the current date
            current_date = date.today().isoformat()

            return render_template('index.html', data=data, selected_company=company, stocks=symbols,current_date=current_date)

    else:

        config_file_path = './config_files/config.ini'
        reader = ConfigReader(config_file_path)
        reader.read_config()

        db_path = reader.get_db_path()
        stk_db_handler = StockDataManager(db_path)

        symbols = get_company_names()
        print("^^^^^^^^Company names - ",symbols)

        # Get the selected company from the query parameters
        company = request.args.get('company', '')
        print("Selected company:", company)
        print("GET Request - query parameters:", request.args)

        data = stk_db_handler.fetch_data()
        stk_db_handler.disconnect()

        # Get the current date
        current_date = date.today().isoformat()

        return render_template('index.html', data=data, selected_company=company, stocks=symbols,current_date=current_date)

if __name__ == '__main__':
    app.run()
