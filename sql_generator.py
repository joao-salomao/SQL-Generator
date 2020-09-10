import numpy
import pandas as pd

ALLOWED_EXTENSIONS = {'xlsx', 'csv'}
ALLOWED_OPERATIONS = {'insert', 'update', 'delete'}

def file_is_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def operation_is_allowed(operation):
    return operation in ALLOWED_OPERATIONS
    
def parse_value_to_sql_builder(value):
    if isinstance(value, str) or isinstance(value, pd._libs.tslibs.timestamps.Timestamp):
        return "'{}'".format(value)
    if isinstance(value, numpy.int64) or isinstance(value, numpy.float64):
        return "{}".format(str(value))

def create_insert_sql(df, table_name):
    sql = 'INSERT INTO ' + table_name + '('
    columns = df.columns
    len_columns = len(columns)
    
    for i in range(len_columns):
        if i < len_columns - 1:
            sql = sql + columns[i] + ', '
        else:
            sql = sql + columns[i] + ') VALUES '

    temp = ''
    formatter = ''
    for i in range(df.shape[0]):
        for k in range(len_columns):
            value = parse_value_to_sql_builder(df[columns[k]][i])
            if k == 0:
                formatter = "({}, "
                temp = formatter.format(value)
            elif k < len_columns-1:
                formatter = temp + "{}, "
                temp = formatter.format(value)
            else:
                formatter = temp + "{})"
                temp = formatter.format(value)
    
        if i < df.shape[0] - 1 :
            sql = sql + temp + ', '
        else:
            sql = sql + temp + ';'
    return sql

def create_update_sql(df, table_name):
    sql = ''
    columns = df.columns
    len_columns = len(columns)
    base = 'UPDATE ' + table_name + ' SET'

    formatter = ''
    temp = base
    for i in range(df.shape[0]):
        for k in range(len_columns):
            column = columns[k]
            value = parse_value_to_sql_builder(df[columns[k]][i])
            if k < len_columns - 2:
                formatter = temp + " " + column + " = {},"
                temp = formatter.format(value)
            elif k < len_columns - 1:
                formatter = temp + " " + column + " = {}"
                temp = formatter.format(value)
            else:
                formatter = temp + " " + column + " {}; "
                temp = formatter.format(str(df[columns[k]][i]))
        sql = sql + temp
        temp = base
    return sql.strip()


def create_delete_sql(df, table_name):
    sql = ''
    columns = df.columns
    len_columns = len(columns)
    base = 'DELETE FROM ' + table_name + ' WHERE'
    formatter = ''
    temp = base

    for i in range(df.shape[0]):
        for k in range(len_columns):
            column = columns[k]
            value = parse_value_to_sql_builder(df[columns[k]][i])
            if k < len_columns - 1:
                formatter = temp + " " + column + " = {} AND"
                temp = formatter.format(value)
            else:
                formatter = temp + " " + column + " = {}; "
                temp = formatter.format(value)
        sql = sql + temp
        temp = base

    return sql.strip()

def get_dataframe(file, filename):
    if file_is_allowed(filename) == False:
        raise Exception("File not allowed")

    try:
        ext = filename.rsplit('.', 1)[1]
        if ext == 'xlsx':
            return pd.read_excel(file, sheet_name='Sheet1')
        return pd.read_csv(file)
    except Exception as e:
        raise e

def generate_sql(file, filename, table_name, operation):
    if operation_is_allowed(operation) == False:
        raise Exception('Operation not allowed')
    
    df = get_dataframe(file, filename)
    return {
        'insert': create_insert_sql,
        'update': create_update_sql,
        'delete': create_delete_sql
    }[operation](df, table_name)