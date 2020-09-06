import sys
import sql_generator as g


## Install to work with Excel ##
# pip install xlrd


reload(sys)
systemEncoder = sys.getfilesystemencoding()
sys.setdefaultencoding(systemEncoder)

def validate_args():
    if len(sys.argv) < 4:
        print('> To few arguments <')
        print('You must pass the operation, the table name and the name of the file to be read')
        print('Example: python cli_app.py insert users users.xlsx')
        return False

    if g.operation_is_allowed(sys.argv[1]) == False:
        print('> Operation not allowed <')
        print('The allowed operations are: insert, update, delete.')
        return False

    if g.file_is_allowed(sys.argv[3]) == False:
        print('> File not allowed <')
        print('The allowed extensions are: xlsx and csv.')
        return False

def main():
    if validate_args() == False:
        return
    operation = sys.argv[1]
    table_name = sys.argv[2]
    file = sys.argv[3]
    sql = g.generate_sql(file, table_name, operation)

    open("generated_sql.sql", "w").write(sql)
    print('SQL successfully generated !')

main()