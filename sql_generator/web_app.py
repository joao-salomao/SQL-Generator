from flask import Flask, render_template, request, flash
from sql_generator import generate_sql, operation_is_allowed, file_is_allowed

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'TOP_SECRET'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and validate_request() == True:
        file = request.files['file']
        operation = request.form['operation']
        table_name = request.form['table_name']

        try:
            sql = generate_sql(file, file.filename, table_name, operation)
            return render_template('generated_sql.html', sql=sql)
        except:
            flash('Some error occurred when generating the SQL. Try Again.')

    return render_template('form.html')


def validate_request() -> bool:
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

    if file_is_allowed(request.files['file'].filename) == False:
        flash('File not allowed')
        is_valid = False

    if operation_is_allowed(request.form['operation']) == False:
        flash('Invalid operation')
        is_valid = False
    return is_valid

if (__name__ == '__main__'):
    app.config["ENV"] = 'development'
    app.run(host='0.0.0.0', port=5000, debug=True)