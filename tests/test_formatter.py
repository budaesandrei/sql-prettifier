import unittest
from sql_prettifier.formatter import SqlFormatter

class TestSqlFormatter(unittest.TestCase):
    def test_format(self):
        formatter = SqlFormatter()
        sql_string = "SELECT * FROM table WHERE condition"
        expected_result = "SELECT *\nFROM table\nWHERE condition"
        formatted_sql = formatter.format(sql_string)
        self.assertEqual(formatted_sql, expected_result)

if __name__ == '__main__':
    unittest.main()