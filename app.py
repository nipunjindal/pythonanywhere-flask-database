# app.py
import os
from flask import Flask, render_template
import datetime
import pytz
import pandas as pd

app = Flask(__name__)


def read_csv_data(csv_path):
    # Read CSV data using Pandas
    csv_data = pd.read_csv(csv_path)
    csv_data = csv_data.reset_index()  # Add index column
    return csv_data


def get_modified_date(csv_path):
    last_modified = os.path.getmtime(csv_path)
    modified_datetime = datetime.datetime.fromtimestamp(last_modified)
    ist_timezone = pytz.timezone("Asia/Kolkata")
    modified_datetime_ist = modified_datetime.astimezone(ist_timezone)
    modified_date = modified_datetime_ist.strftime("%a, %b %d, %Y, %Z %I:%M %p")
    return modified_date


@app.route('/')
def index():
    # Read data from CSV file
    csv_path = 'data/data.csv'
    csv_data = read_csv_data(csv_path)

    # Get last modified date of CSV file
    modified_date = get_modified_date(csv_path)

    return render_template('index.html', csv_data=csv_data, modified_date=modified_date)


if __name__ == '__main__':
    app.run(debug=True)
