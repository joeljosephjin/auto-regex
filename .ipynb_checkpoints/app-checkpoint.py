from flask import Flask, render_template, request, render_template_string, redirect, send_file
import pandas as pd
import re


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
        for i, tag in enumerate(eval(row.to_list()[1])):
            out+=f"""<div class='chip' id='row_{index}_col_1_i_{i}'>{tag}</div><span class='closebtn' onclick='closeTag(this)'>&times;</span>"""
        out+="</td>\n"
        out+=f"\n</tr>\n"
    out+="""  </tbody>
</table>"""
    # print('out:',out)
    return out

data = pd.read_csv('data/truth_uploaded.csv')

@app.route('/new_data_table')
def table():
    data = pd.read_csv('data/truth_uploaded.csv')
    return render_template('new_data_table.html', tables=[table_to_html(data)], titles=[''])

@app.route('/upload_csv', methods = ['GET', 'POST'])
def upload_csv():
    f = request.files['file']
    f.save('data/truth_uploaded.csv')
    data = pd.read_csv('data/truth_uploaded.csv')
    return render_template('new_data_table.html', tables=[table_to_html(data)], titles=[''])

@app.route('/save_data', methods = ['POST'])
def save_data():
    data = pd.read_csv('data/truth_uploaded.csv')
    if request.method == 'POST':
        tags_dict = request.json
        # import pdb; pdb.set_trace()
        tags_new_dict = {}
        for key, val in tags_dict.items():
            index = eval(key.split('_')[1])
            tag = val
            if index in tags_new_dict.keys():
                tags_new_dict[index].append(tag)
            else:
                tags_new_dict[index] = [tag]
        for key, val in tags_new_dict.items():
            # import pdb; pdb.set_trace()
            index = key
            tag = val
            data.loc[index,'tags'] = val
    
    # import pdb; pdb.set_trace()
    # print(data)
    data.to_csv('data/truth_uploaded.csv', index=False)
    
    return tags_new_dict

@app.route('/data/truth_uploaded', methods=['GET'])
def download():
    return send_file('data/truth_uploaded.csv', as_attachment=True)

@app.route('/apply_pattern', methods = ['POST'])
def apply_pattern():
    pattern_text = request.json['pattern']
    
    detected_tags = {}
    for index, row in data.iterrows():
        main_text = str(data.loc[index, 'sms'])
        detected_tags[index] = list(set([x.group() for x in re.finditer(pattern_text, main_text)]))
        
    return detected_tags
    