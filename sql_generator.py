import sys
reload(sys)

try:
    import pandas as pd
except ImportError:
    print("Can't find pandas module")
    print("Type the command 'pip install pandas' to install the module")

systemEncoder = sys.getfilesystemencoding()
sys.setdefaultencoding(systemEncoder)


# pip install xlrd

def createInsertSQL(df, tableName):
    sql = 'INSERT INTO ' + tableName + '('
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
    
def createUpdateSQL(df, tableName):
    sql = ''
    columns = df.columns
    lenColumns = len(columns)
    base = 'UPDATE ' + tableName + ' SET '

    formatter = ''
    temp = base
    for i in range(df.shape[0]):
        for k in range(lenColumns):
            value = str(df[columns[k]][i])
            if k < lenColumns - 1:
                formatter = temp + " " + columns[k] + " = '{}',"
                temp = formatter.format(value)
            else:
                formatter = temp + " " + columns[k] + " {}; "
                temp = formatter.format(value)
        sql = sql + temp
        temp = base
    return sql

def main():
    if len(sys.argv) < 4:
        print('To few arguments')
        print('You must pass the operation, the table name and the name of the file to be read')
        print('Example: python sql_generator.py insert users users.xlsx')
        return

    if sys.argv[1] != 'insert' and sys.argv[1] != 'update':
        print('Operation type invalid')
        return

    fileExtension = sys.argv[3].split('.')[1]
    if fileExtension == 'xlsx':
        df = pd.read_excel(sys.argv[3], sheet_name='Sheet1')
    else:
        df = pd.read_csv(sys.argv[3])
    
    
    sql = ''
    tableName = sys.argv[2]
    if sys.argv[1] == 'insert':
        sql = createInsertSQL(df, tableName)
    else:
        sql = createUpdateSQL(df, tableName)

    open("generated_sql.sql", "w").write(sql)
    print('SQL successfully generated !')
main()