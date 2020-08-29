import pandas as pd
from flask import Flask, render_template, request, flash, redirect
from sql_generator import ALLOWED_OPERATIONS, create_insert_sql, create_update_sql, file_is_allowed

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'TOP_SECRET'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if validate_request() == False:
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


def validate_request():
    if 'table_name' not in request.form:
        flash('Table name is required')
        return False
    
    if len(request.form['table_name']) == 0:
        flash('Table name is required')

    if 'file' not in request.files:
        flash('No file part')
        return False

    if request.files['file'].filename == '':
        flash('No selected file')
        return False

    if file_is_allowed(request.files['file'].filename) == False:
        flash('File not allowed')
        return False

    if request.form['operation_type'] not in ALLOWED_OPERATIONS:
        flash('Operation type invalid')
        return False
    return True