from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/new_data_table')
def table():
    # converting csv to html
    data = pd.read_csv('data/truth.csv')
    return render_template('new_data_table.html', tables=[data.to_html()], titles=[''])
