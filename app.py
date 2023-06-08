# app.py
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # Read data from CSV file
    with open('data/data.csv', 'r') as file:
        csv_data = file.read()

    return render_template('index.html', csv_data=csv_data)


if __name__ == '__main__':
    app.run(debug=True)
