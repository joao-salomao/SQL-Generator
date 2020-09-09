from pandas import DataFrame
from unittest import TestCase, main
from sql_generator import operation_is_allowed, file_is_allowed, create_insert_sql

class TestValidations(TestCase):
    def test_should_allow_operation(self):
        self.assertTrue(operation_is_allowed('insert'))
        self.assertTrue(operation_is_allowed('update'))
        self.assertTrue(operation_is_allowed('delete'))

    def test_should_not_allow_operation(self):
        self.assertFalse(operation_is_allowed('create'))
        self.assertFalse(operation_is_allowed('remove'))
        self.assertFalse(operation_is_allowed('use'))

    def test_should_allow_file(self):
        self.assertTrue(file_is_allowed('users.xlsx'))
        self.assertTrue(file_is_allowed('users.csv'))

    def test_should_not_allow_file(self):
        self.assertFalse(file_is_allowed('users.xls'))
        self.assertFalse(file_is_allowed('users.ods'))
        self.assertFalse(file_is_allowed('users.exe'))
        self.assertFalse(file_is_allowed('users.py'))
        self.assertFalse(file_is_allowed('users.ots'))


class TestCreateInsertSQL(TestCase):
    def setUp(self):
        self.data = [
            {
                "table_name": "users",
                "dataframe": DataFrame({
                    'id': [1,2,3],
                    'name': ['Jane', 'Victor', 'Bob'],
                    'salary': [2500.6, 1000.5, 3450.1]
                }),
                "expected": "INSERT INTO users(id, name, salary) VALUES (1, 'Jane', 2500.6), (2, 'Victor', 1000.5), (3, 'Bob', 3450.1);"
            },
            {
                "table_name": "companies",
                "dataframe": DataFrame({
                    'id': [333,414,578, 1234],
                    'company_name': ['Apple', 'AOC', 'Samsung', 'LG'],
                    'market_price': [300000000000, 99999999, 46464646464646, 123123123123]
                }),
                "expected": "INSERT INTO companies(id, company_name, market_price) VALUES (333, 'Apple', 300000000000), (414, 'AOC', 99999999), (578, 'Samsung', 46464646464646), (1234, 'LG', 123123123123);"
            }
        ]

    def test_should_create_insert_sql(self):
        for case in self.data:
            df =case["dataframe"]
            expected = case["expected"]
            table_name = case["table_name"]
            self.assertEqual(expected, create_insert_sql(df, table_name))

if __name__ == '__main__':
    main(verbosity=2)