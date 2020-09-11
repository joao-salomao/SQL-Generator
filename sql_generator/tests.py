from pandas import DataFrame
from unittest import TestCase, main
from sql_generator import create_insert_sql, create_update_sql, create_delete_sql
from sql_generator import operation_is_allowed, file_is_allowed, generate_sql, get_dataframe

class TestSQLGenerator(TestCase):
    def setUp(self):
        self.data_insert = [
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

        self.data_update = [
            {
                "table_name": "accounts",
                "dataframe": DataFrame({
                    'name': ['Jane', 'Victor', 'Bob'],
                    'likes': [3000, 2460, 3450],
                    'WHERE': ['id = 1','id = 2','id = 3'],
                }),
                "expected": "UPDATE accounts SET name = 'Jane', likes = 3000 WHERE id = 1; UPDATE accounts SET name = 'Victor', likes = 2460 WHERE id = 2; UPDATE accounts SET name = 'Bob', likes = 3450 WHERE id = 3;"
            },
            {
                "table_name": "salaries",
                "dataframe": DataFrame({
                    'salary': [3000.5, 2460.9, 3450.2],
                    'WHERE': ['user_id = 1','user_id = 2','user_id = 3'],
                }),
                "expected": "UPDATE salaries SET salary = 3000.5 WHERE user_id = 1; UPDATE salaries SET salary = 2460.9 WHERE user_id = 2; UPDATE salaries SET salary = 3450.2 WHERE user_id = 3;"
            },
        ]

        self.data_delete = [
            {
                "table_name": "accounts",
                "dataframe": DataFrame({
                    'name': ['Jane', 'Victor', 'Bob'],
                    'likes': [3000, 2460, 3450],
                }),
                "expected": "DELETE FROM accounts WHERE name = 'Jane' AND likes = 3000; DELETE FROM accounts WHERE name = 'Victor' AND likes = 2460; DELETE FROM accounts WHERE name = 'Bob' AND likes = 3450;"
            },
            {
                "table_name": "salaries",
                "dataframe": DataFrame({
                    'salary': [3000.5, 2460.9, 3450.2],
                    'user_id': [1,2,3],
                }),
                "expected": "DELETE FROM salaries WHERE salary = 3000.5 AND user_id = 1; DELETE FROM salaries WHERE salary = 2460.9 AND user_id = 2; DELETE FROM salaries WHERE salary = 3450.2 AND user_id = 3;"
            },
        ]

    def test_should_create_insert_sql(self):
        for case in self.data_insert:
            df =case["dataframe"]
            expected = case["expected"]
            table_name = case["table_name"]
            result = create_insert_sql(df, table_name)

            self.assertIsInstance(result, str)
            self.assertEqual(expected, result)

    def test_should_create_update_sql(self):
        for case in self.data_update:
            df =case["dataframe"]
            expected = case["expected"]
            table_name = case["table_name"]
            result = create_update_sql(df, table_name)

            self.assertIsInstance(result, str)
            self.assertEqual(expected, result)


    def test_should_create_delete_sql(self):
        for case in self.data_delete:
            df =case["dataframe"]
            expected = case["expected"]
            table_name = case["table_name"]
            result = create_delete_sql(df, table_name)

            self.assertIsInstance(result, str)
            self.assertEqual(expected, result)

    def test_should_generate_sql(self):
        result_insert = generate_sql('files/test_insert.xlsx', 'files/test_insert.xlsx', 'users', 'insert')
        result_update = generate_sql('files/test_update.xlsx','files/test_update.xlsx', 'users', 'update')
        result_delete = generate_sql('files/test_delete.xlsx', 'files/test_delete.xlsx', 'users', 'delete')

        self.assertIsInstance(result_insert, str)
        self.assertTrue(len(result_insert) > 0)

        self.assertIsInstance(result_update, str)
        self.assertTrue(len(result_update) > 0)

        self.assertIsInstance(result_delete, str)
        self.assertTrue(len(result_delete) > 0)


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

    def test_should_get_dataframe(self):
        self.assertIsInstance(get_dataframe('files/test_insert.xlsx', 'files/test_insert.xlsx'), DataFrame)
        self.assertIsInstance(get_dataframe('files/test_update.xlsx', 'files/test_update.xlsx'), DataFrame)
        self.assertIsInstance(get_dataframe('files/test_delete.xlsx', 'files/test_delete.xlsx'), DataFrame)

        with self.assertRaises(Exception):
            self.assertIsInstance(get_dataframe('asdasd', 'hjgh.asd'), DataFrame)
            self.assertIsInstance(get_dataframe('asdasd', 'qweq.gasd'), DataFrame)
            self.assertIsInstance(get_dataframe('asdasd', 'qwewq.qweq'), DataFrame)


if __name__ == '__main__':
    main(verbosity=2)