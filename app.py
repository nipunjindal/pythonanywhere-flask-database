from flask import Flask, render_template, request, jsonify, session
import os
import datetime
import pytz
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management


def read_csv_data(csv_path='data/data.csv'):
    # Read CSV data from session if it exists
    if 'csv_data' in session:
        csv_data_json = session['csv_data']
        csv_data = pd.read_json(csv_data_json)
        return csv_data

    # Read CSV data from disk
    csv_data = pd.read_csv(csv_path, keep_default_na=False)

    # Store CSV data in session
    csv_data_json = csv_data.to_json(orient='records')
    session['csv_data'] = csv_data_json

    return csv_data


def save_csv_data(csv_data, csv_path='data/data.csv'):
    # Save CSV data using Pandas
    csv_data.to_csv(csv_path, index=False)
    # Update the CSV data in session
    csv_data_json = csv_data.to_json(orient='records')
    session['csv_data'] = csv_data_json


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

    # Get last modified date of CSV file
    modified_date = get_modified_date()

    return render_template('index.html', csv_data=csv_data, modified_date=modified_date)


@app.route('/edit', methods=['POST'])
def edit():
    # Retrieve the edited data from the request form
    row_index = int(request.form['editRowIndex'])
    osn_no = request.form['editOSNNo']
    party_name = request.form['editPartyName']
    next_date = request.form['editNextDate']
    work_done = request.form.get('editWorkDone', '')

    # Replace backticks (`) with escape sequence (\`) in osn_no and party_name
    osn_no = replace_backticks(osn_no)
    party_name = replace_backticks(party_name)

    # Convert the next date to the desired format (MM/DD/YY)
    datetime_obj = datetime.datetime.strptime(next_date, "%Y-%m-%d")
    formatted_next_date = datetime_obj.strftime("%m/%d/%y 00:00:00")

    # Read data from session
    csv_data = read_csv_data()

    if row_index == -1:
        # Create a new row in the CSV data
        new_row = pd.DataFrame({
            'index': [csv_data.index.max() + 1],
            'OSN_NO': [osn_no],
            'Party_Name': [party_name],
            'Next_Date': [formatted_next_date],
            'Work_Done': [work_done]
        })
        csv_data = pd.concat([csv_data, new_row])
    else:
        # Update the corresponding row in the CSV data
        csv_data.loc[row_index, 'OSN_NO'] = osn_no
        csv_data.loc[row_index, 'Party_Name'] = party_name
        csv_data.loc[row_index, 'Next_Date'] = formatted_next_date
        csv_data.loc[row_index, 'Work_Done'] = work_done

    # Save the CSV data back to the file and update session
    save_csv_data(csv_data)

    # Convert DataFrame to list of dictionaries
    csv_data_dict = csv_data.to_dict(orient='records')

    # Return the updated CSV data and modified date as JSON response
    response_data = {
        'status': 'success',
        'csv_data': csv_data_dict,
        'modified_date': get_modified_date()
    }

    return jsonify(response_data)


def replace_backticks(value):
    return value.replace('`', r'\`')


if __name__ == '__main__':
    app.run(debug=True)
