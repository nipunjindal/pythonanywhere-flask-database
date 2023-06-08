# app.py
import os
from flask import Flask, render_template
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    # Read data from CSV file
    csv_path = 'data/data.csv'
    with open(csv_path, 'r') as file:
        csv_data = file.read()

    # Get last modified date of CSV file
    last_modified = os.path.getmtime(csv_path)

    return render_template('index.html', csv_data=csv_data, last_modified=last_modified)


if __name__ == '__main__':
    app.run(debug=True)
