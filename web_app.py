import pandas as pd
from flask import Flask, render_template, request, flash, redirect
from sql_generator import ALLOWED_OPERATIONS, ALLOWED_EXTENSIONS,create_insert_sql, create_update_sql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOP_SECRET'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        validate_request()

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


def validate_request():
    if 'table_name' not in request.form:
        flash('Table name is required')
        return redirect(request.url)
    
    if len(request.form['table_name']) == 0:
        flash('Table name is required')
        return redirect(request.url)

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    if request.files['file'].filename == '':
        flash('No selected file')
        return redirect(request.url)

    if allowed_file(request.files['file'].filename) == False:
        flash('File not allowed')
        return redirect(request.url)

    if request.form['operation_type'] not in ALLOWED_OPERATIONS:
        flash('Operation type invalid')
        return redirect(request.url)