import pandas as pd
from flask import Flask, render_template, request, flash, redirect

ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOP_SECRET'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'table_name' not in request.form:
            flash('Table name is required')
            return redirect(request.url)
        
        if len(request.form['table_name']) == 0:
            flash('Table name is required')
            return redirect(request.url)

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        if request.files['file'].filename == '':
            flash('No selected file')
            return redirect(request.url)

        if allowed_file(request.files['file'].filename) == False:
            flash('File not allowed')
            return redirect(request.url)

        file = request.files['file']
        table_name = request.form['table_name']
        operation_type = request.form['operation_type']

        df = pd.read_excel(file, sheet_name='Sheet1')
        sql = ''

        if operation_type == 'insert':
            sql = create_insert_sql(df, table_name)

        if operation_type == 'update':
            sql = create_update_sql(df, table_name)   
            
        return render_template('generated_sql.html', sql=sql)

    return render_template('upload_file.html')

def create_insert_sql(df, table_name):
    sql = 'INSERT INTO ' + table_name + '('
    columns = df.columns
    lenColumns = len(columns)
    
    for i in range(lenColumns):
        if i < lenColumns - 1:
            sql = sql + columns[i] + ','
        else:
            sql = sql + columns[i] + ') VALUES '

    temp = ''
    formatter = ''
    for i in range(df.shape[0]):
        for k in range(lenColumns):
            value = str(df[columns[k]][i])
            if k == 0:
                formatter = "('{}',"
                temp = formatter.format(value)
            elif k < lenColumns-1:
                formatter = temp + "'{}',"
                temp = formatter.format(value)
            else:
                formatter = temp + "'{}')"
                temp = formatter.format(value)
    
        if i < df.shape[0] - 1 :
            sql = sql + temp + ','
        else:
            sql = sql + temp + ';'
    return sql

def create_update_sql(df, table_name):
    sql = ''
    columns = df.columns
    lenColumns = len(columns)
    base = 'UPDATE ' + table_name + ' SET '

    formatter = ''
    temp = base
    for i in range(df.shape[0]):
        for k in range(lenColumns):
            column = columns[k]
            value = str(df[columns[k]][i])

            if k < lenColumns - 1:
                formatter = temp + " " + column + " = '{}',"
                temp = formatter.format(value)
            else:
                formatter = temp + " " + column + " {}; "
                temp = formatter.format(value)
        sql = sql + temp
        temp = base
    return sql