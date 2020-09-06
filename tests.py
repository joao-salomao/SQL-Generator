import unittest
from sql_generator import operation_is_allowed, file_is_allowed

class TestValidations(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()