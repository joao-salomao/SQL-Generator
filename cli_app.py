from sys import argv
from sql_generator import generate_sql, operation_is_allowed, file_is_allowed

def validate_args():
    if len(argv) < 4:
        print('> To few arguments <')
        print('You must pass the operation, the table name and the name of the file to be read')
        print('Example: python cli_app.py insert users users.xlsx')
        return False

    if operation_is_allowed(argv[1]) == False:
        print('> Operation not allowed <')
        print('The allowed operations are: insert, update, delete.')
        return False

    if file_is_allowed(argv[3]) == False:
        print('> File not allowed <')
        print('The allowed extensions are: xlsx and csv.')
        return False

def main():
    if validate_args() == False:
        return
    operation = argv[1]
    table_name = argv[2]
    file = argv[3]
    sql = generate_sql(file, table_name, operation)

    open("generated_sql.sql", "w").write(sql)
    print('SQL successfully generated !')

main()