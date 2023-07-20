from flask import Flask, render_template, request
import logging
from datetime import datetime,time,date

from config_reader import ConfigReader 
from stock_db_handler import StockDataManager
from time_util import TimeUtil
from logger import Logger

import json

def extract_company_name(stock):
    return stock.split(" ")

def is_company_available(company):
    # Return True if the company is available, False otherwise
    symbols = get_company_names()
    return company in symbols

def get_company_names():
    reader = ConfigReader()
    reader.read_config()

    db_path = reader.get_db_path()
    stk_db_handler = StockDataManager(db_path)

    return stk_db_handler.fetch_companies()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/stocks/', methods=['GET', 'POST'])
def display_table():

    if request.method == 'POST':

        # Validate the incoming data - range - format etc.
        # Get the selected company from the form submission
        company = request.form.get('company')
        start_date = request.form.get('start-date')
        end_date = request.form.get('end-date')

        print(company, start_date, end_date)

        Logger.get_instance().log(logging.INFO,'@app.route [POST Request]','display_table : In coming request with following Parameters: '
                                 + '\nCompany Name: ' + company + '\nStart Date: ' + start_date + '\nEnd Date: ' + end_date + '',)

        # Validate the incoming data
        errors = []

        # Validate start date
        try:
            start_datetm = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid start date format. Please use YYYY-MM-DD.")
            Logger.get_instance().log(logging.WARNING,'@app.route [POST Request]','display_table : Invalid start date format. Please use YYYY-MM-DD.')

        # Validate end date
        try:
            end_datetm = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid end date format. Please use YYYY-MM-DD.")
            Logger.get_instance().log(logging.WARNING,'@app.route [POST Request]','display_table : Invalid end date format. Please use YYYY-MM-DD.')

        # Check if start date is before end date
        if start_datetm and end_datetm and start_datetm > end_datetm:
            errors.append("Start date cannot be after end date.")
            Logger.get_instance().log(logging.WARNING,'@app.route [POST Request]','display_table : Start date cannot be after end date.')

        # Check if the selected company is available in the database
        if not is_company_available(company):
            errors.append("Provided company data is not available in the database. Check the company name.")
            Logger.get_instance().log(logging.WARNING,'@app.route [POST Request]','display_table : Provided company data is not available in the database. Check the company name.')

        # If there are any validation errors, render the template with the error messages
        if errors:
            symbols = get_company_names()  # Replace with your logic to fetch company symbols
            current_date = date.today().isoformat()
            return render_template('index.html', errors=errors, stocks=symbols, current_date=current_date)
        else:

            time_util = TimeUtil()
            reader = ConfigReader()
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

            Logger.get_instance().log(logging.DEBUG,'@app.route [POST Request]','display_table : fetching data from database with parameters: '
                                     + '\nSelected company name:' + company + '\nLocalize Start date:' + l_start_date_time 
                                     +'\nLocalize End date:' + l_end_date_time)

            if company:
                # Fetch data from the database based on the selected company and date range
                data = stk_db_handler.fetch_data_by_company_and_dates(company, l_start_date_time, l_end_date_time)

            symbols = stk_db_handler.fetch_companies()
            stk_db_handler.disconnect()

            # Get the current date
            current_date = date.today().isoformat()

            Logger.get_instance().log(logging.DEBUG,'@app.route [POST Request]','display_table : Render the page with the following data: '
                                      + '\List of companies Name available in database: ' + str(symbols) + '\nCurrent date: ' + current_date
                                      + '\nSelected company name: ' + company + '\nData: ' + str(data))

            return render_template('index.html', data=data, selected_company=company, stocks=symbols,current_date=current_date)

    else:

        # Get the selected company from the query parameters
        company = request.args.get('company', '')
        print(type(company))
        Logger.get_instance().log(logging.INFO,'@app.route [GET Request]','display_table : In coming request with following Parameters: '
                                  + '\nCompany Name: ' + company + 'Request Arguments: ' + str(request.args))
        

        reader = ConfigReader()
        reader.read_config()

        db_path = reader.get_db_path()
        stk_db_handler = StockDataManager(db_path)

        symbols = get_company_names()

        Logger.get_instance().log(logging.DEBUG,'@app.route [GET Request]','display_table : List of Companies or Stocks names stored in the Database : ' 
                                  + str(symbols))

        data = stk_db_handler.fetch_data()
        stk_db_handler.disconnect()

        # Get the current date
        current_date = date.today().isoformat()
        if company is "":
            company = symbols[0]
        return render_template('index.html', data=data[:900], selected_company=company, stocks=symbols,current_date=current_date)

''' @app.route('/fetch-data', methods=['POST'])
def fetch_data():

    reader = ConfigReader()
    reader.read_config()

    db_path = reader.get_db_path()
    stk_db_handler = StockDataManager(db_path)

    # offset = 

    rows,columns = stk_db_handler.fetch_data(offset,limit)
    stk_db_handler.disconnect()

    # Create a list of dictionaries, where each dictionary represents a row
    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))

    # Convert the result to JSON
    json_result = json.dumps(result)

    # Print or return the JSON result
    print(json_result)

    query = request.json.get('query', '')
    offset = int(request.json.get('offset', 0))
    limit = int(request.json.get('limit', 10))

    
    # Filter data based on query
    filtered_data = [item for item in data if query.lower() in item['name'].lower()]
    
    # Apply offset and limit
    paginated_data = filtered_data[offset:offset+limit]
    
    return jsonify(paginated_data)'''

if __name__ == '__main__':
    app.run()
