
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

ALLOWED_OPERATIONS = {'insert', 'update'}

def file_is_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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