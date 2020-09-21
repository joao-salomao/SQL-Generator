from typing import Union
from numpy import int64, float64
from werkzeug.datastructures import FileStorage
from pandas import read_excel, read_csv, DataFrame
from pandas._libs.tslibs.timestamps import Timestamp

ALLOWED_EXTENSIONS = {'xlsx', 'csv'}
ALLOWED_OPERATIONS = {'insert', 'update', 'delete'}

def file_is_allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def operation_is_allowed(operation: str) -> bool:
    return operation in ALLOWED_OPERATIONS
    
def parse_value_to_sql_builder(value: Union[str, int64, float64, Timestamp]) -> str:
    if isinstance(value, str) or isinstance(value, Timestamp):
        return "'{}'".format(value)
    if isinstance(value, int64) or isinstance(value, float64):
        return "{}".format(str(value))
    raise Exception("Error parsing value to sql builder")

def create_insert_sql(df: DataFrame, table_name: str) -> str:
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

def create_update_sql(df: DataFrame, table_name: str) -> str:
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


def create_delete_sql(df: DataFrame, table_name: str) -> str:
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

def get_dataframe(file: Union[FileStorage, str], filename: str) -> DataFrame:
    if file_is_allowed(filename) == False:
        raise Exception("File not allowed")

    try:
        ext = filename.rsplit('.', 1)[1]
        if ext == 'xlsx':
            return read_excel(file, sheet_name='Sheet1')
        return read_csv(file)
    except Exception as e:
        raise e

def generate_sql(file: Union[FileStorage, str], filename: str, table_name: str, operation: str) -> str:
    if operation_is_allowed(operation) == False:
        raise Exception('Operation not allowed')
    
    df = get_dataframe(file, filename)
    return {
        'insert': create_insert_sql,
        'update': create_update_sql,
        'delete': create_delete_sql
    }[operation](df, table_name)