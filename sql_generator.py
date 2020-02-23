import sys
import pandas as pd

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
            if k == 0:
                formatter = "('{}',"
                temp = formatter.format(str(df[columns[k]][i]))
            elif k < lenColumns-1:
                formatter = temp + "'{}',"
                temp = formatter.format(str(df[columns[k]][i]))
            else:
                formatter = temp + "'{}')"
                temp = temp = formatter.format(str(df[columns[k]][i]))
    
        if i < df.shape[0] - 1 :
            sql = (sql +
                temp + ',')
        else:
            sql = (sql +
                temp + ';')
            
    print(sql)
    return sql


def main():
    if len(sys.argv) < 4:
        print('To few arguments')
        print('You must pass the operation, the table name and the name of the file to be read')
        print('Example: main.py insert users users.xlsx')
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

    f = open("generated_sql.sql", "w")
    f.write(sql)

main()