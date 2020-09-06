import sql_generator as g
from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'TOP_SECRET'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and validate_request() == True:
        file = request.files['file']
        table_name = request.form['table_name']
        operation_type = request.form['operation_type']
       
        sql = g.OPERATION_HANDLER[operation_type](file, table_name)   
        return render_template('generated_sql.html', sql=sql)

    return render_template('form.html')


def validate_request():
    is_valid = True

    if len(request.form['table_name']) == 0:
        flash('Table name is required')
        is_valid = False

    if 'file' not in request.files:
        flash('No file part')
        is_valid = False

    if len(request.files['file'].filename) == 0:
        flash('No selected file')
        is_valid = False

    if g.file_is_allowed(request.files['file'].filename) == False:
        flash('File not allowed')
        is_valid = False

    if request.form['operation_type'] not in g.ALLOWED_OPERATIONS:
        flash('Operation type invalid')
        is_valid = False
    return is_valid