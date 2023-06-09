# app.py
import os
from flask import Flask, render_template, request
import datetime
import pytz
import pandas as pd

app = Flask(__name__)

# Global variable to store the CSV data
csv_data = None


def read_csv_data(csv_path):
    # Read CSV data using Pandas
    data = pd.read_csv(csv_path)
    data = data.reset_index()  # Add index column
    return data


def save_csv_data(csv_path):
    # Save CSV data using Pandas
    csv_data.to_csv(csv_path, index=False)


def get_modified_date(csv_path):
    last_modified = os.path.getmtime(csv_path)
    modified_datetime = datetime.datetime.fromtimestamp(last_modified)
    ist_timezone = pytz.timezone("Asia/Kolkata")
    modified_datetime_ist = modified_datetime.astimezone(ist_timezone)
    modified_date = modified_datetime_ist.strftime("%a, %b %d, %Y, %Z %I:%M %p")
    return modified_date


@app.route('/')
def index():
    global csv_data

    # Read data from CSV file
    csv_path = 'data/data.csv'
    csv_data = read_csv_data(csv_path)

    # Get last modified date of CSV file
    modified_date = get_modified_date(csv_path)

    return render_template('index.html', csv_data=csv_data, modified_date=modified_date)


@app.route('/edit', methods=['POST'])
def edit():
    global csv_data

    # Retrieve the edited data from the request form
    row_index = int(request.form['row_index'])
    osn_no = request.form['editOSNNo']
    party_name = request.form['editPartyName']
    next_date = request.form['editNextDate']

    # Convert the next date to the desired format (MM/DD/YY)
    datetime_obj = datetime.datetime.strptime(next_date, "%Y-%m-%d")
    formatted_next_date = datetime_obj.strftime("%m/%d/%y")

    # Update the corresponding row in the CSV data
    csv_data.loc[row_index, 'OSN_NO'] = osn_no
    csv_data.loc[row_index, 'Party_Name'] = party_name
    csv_data.loc[row_index, 'Next_Date'] = formatted_next_date

    # Save the CSV data back to the file
    save_csv_data('data/data.csv')

    return 'Success'


if __name__ == '__main__':
    app.run(debug=True)
