import sql_generator as g
from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'TOP_SECRET'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and validate_request() == True:
        file = request.files['file']
        table_name = request.form['table_name']
        operation = request.form['operation']

        sql = g.generate_sql(file, table_name, operation)
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

    if  g.operation_is_allowed(request.form['operation']) == False:
        flash('Invalid operation')
        is_valid = False
    return is_valid