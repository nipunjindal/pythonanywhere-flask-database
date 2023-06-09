# app.py
import os
from flask import Flask, render_template, request, jsonify
import datetime
import pytz
import pandas as pd

app = Flask(__name__)


def read_csv_data(csv_path='data/data.csv'):
    # Read CSV data using Pandas
    data = pd.read_csv(csv_path)
    return data


def save_csv_data(csv_data, csv_path='data/data.csv'):
    # Save CSV data using Pandas
    csv_data.to_csv(csv_path, index=False)


def get_modified_date(csv_path='data/data.csv'):
    last_modified = os.path.getmtime(csv_path)
    modified_datetime = datetime.datetime.fromtimestamp(last_modified)
    ist_timezone = pytz.timezone("Asia/Kolkata")
    modified_datetime_ist = modified_datetime.astimezone(ist_timezone)
    modified_date = modified_datetime_ist.strftime("%a, %b %d, %Y, %Z %I:%M %p")
    return modified_date


@app.route('/')
def index():
    # Read data from CSV file
    csv_data = read_csv_data()
    csv_data = csv_data.reset_index()  # Add index column

    # Get last modified date of CSV file
    modified_date = get_modified_date()

    return render_template('index.html', csv_data=csv_data, modified_date=modified_date)


@app.route('/edit', methods=['POST'])
def edit():
    csv_data = read_csv_data()

    # Retrieve the edited data from the request form
    row_index = int(request.form['editRowIndex'])
    osn_no = request.form['editOSNNo']
    party_name = request.form['editPartyName']
    next_date = request.form['editNextDate']

    # Convert the next date to the desired format (MM/DD/YY)
    datetime_obj = datetime.datetime.strptime(next_date, "%Y-%m-%d")
    formatted_next_date = datetime_obj.strftime("%m/%d/%y 00:00:00")

    if row_index == -1:
        # Create a new row in the CSV data
        new_row = pd.DataFrame({'OSN_NO': [osn_no], 'Party_Name': [party_name], 'Next_Date': [formatted_next_date]})
        csv_data = pd.concat([csv_data, new_row], ignore_index=True)
    else:
        # Update the corresponding row in the CSV data
        csv_data.loc[row_index, 'OSN_NO'] = osn_no
        csv_data.loc[row_index, 'Party_Name'] = party_name
        csv_data.loc[row_index, 'Next_Date'] = formatted_next_date

    # Save the CSV data back to the file
    save_csv_data(csv_data)

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
