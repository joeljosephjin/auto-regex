from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

# make function that mimics to_html
def table_to_html(df):
    out = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>"""
    # get the column names
    cols = df.columns.to_list()
    for col in cols:
        out+=f"      <th>{col}</th>\n"
    out+="""    </tr>
  </thead>
  <tbody>"""
    for index, row in df.iterrows():
        out+="\n<tr>\n"
        out+=f"\n<th>{index}</th>\n"
        # for i, item in enumerate(row.to_list()):
        out+=f"\n<td id='row_{index}_col_0'>{row.to_list()[0]}</td>\n"
        out+=f"\n<td id='row_{index}_col_1'>"
        for tag in eval(row.to_list()[1]):
            out+=f"<button>{tag}</buton>"
        out+="</td>\n"
        out+=f"\n</tr>\n"
    out+="""  </tbody>
</table>"""
    # print('out:',out)
    return out

@app.route('/new_data_table')
def table():
    # converting csv to html
    data = pd.read_csv('data/truth.csv')
    # return render_template('new_data_table.html', tables=[data.to_html()], titles=[''])
    return render_template('new_data_table.html', tables=[table_to_html(data)], titles=[''])
