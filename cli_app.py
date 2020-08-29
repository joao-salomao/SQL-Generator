import sys
from sql_generator import ALLOWED_OPERATIONS, create_insert_sql, create_update_sql
try:
    import pandas as pd
except ImportError:
    print("Can't find pandas module")
    print("Type the command 'pip install pandas' to install the module")


## Install to work with Excel ##
# pip install xlrd


##  Enable to fix encoding errors ##
#reload(sys)
#systemEncoder = sys.getfilesystemencoding()
#sys.setdefaultencoding(systemEncoder)

def main():
    if len(sys.argv) < 4:
        print('To few arguments')
        print('You must pass the operation, the table name and the name of the file to be read')
        print('Example: python cli_app.py insert users users.xlsx')
        return

    if sys.argv[1] not in ALLOWED_OPERATIONS:
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
        sql = create_insert_sql(df, tableName)
    else:
        sql = create_update_sql(df, tableName)

    open("generated_sql.sql", "w").write(sql)
    print('SQL successfully generated !')

main()