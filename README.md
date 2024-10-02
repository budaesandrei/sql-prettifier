# sql-prettifier

`sql-prettifier` is a Python library that provides a comprehensive set of configuration options for formatting SQL strings. It uses the `sqlparse` library for parsing and formatting SQL.

## Installation

You can install `sql-prettifier` using pip:

```shell
pip install sql-prettifier
```

## Usage

To use `sql-prettifier`, first import the `SqlFormatter` class from the `sql_prettifier` module:

```python
from sql_prettifier.formatter import SqlFormatter
```

Then, create an instance of the `SqlFormatter` class with the desired configuration options:

```python
formatter = SqlFormatter(indent_width=4, keyword_case='upper')
```

The available configuration options are:

- `indent_width` (int): The number of spaces to use for indentation. Default is 2.
- `keyword_case` (str): The case to use for SQL keywords. Options are 'upper', 'lower', and 'capitalize'. Default is 'capitalize'.
- `identifier_case` (str): The case to use for SQL identifiers (table names, column names, etc.). Options are 'upper', 'lower', and 'capitalize'. Default is 'lower'.

Once you have created the `SqlFormatter` instance, you can use the `.format(sql_string)` method to format your SQL string:

```python
formatted_sql = formatter.format('SELECT * FROM my_table WHERE id = 1')
print(formatted_sql)
```

This will output the formatted SQL string according to the specified configuration options.

## Examples

Here are some examples of using `sql-prettifier`:

```python
from sql_prettifier.formatter import SqlFormatter

# Example 1: Format SQL with default options
formatter = SqlFormatter()
formatted_sql = formatter.format('SELECT * FROM my_table WHERE id = 1')
print(formatted_sql)

# Example 2: Format SQL with custom options
formatter = SqlFormatter(indent_width=4, keyword_case='upper')
formatted_sql = formatter.format('SELECT * FROM my_table WHERE id = 1')
print(formatted_sql)
```

## Contributing

Contributions to `sql-prettifier` are welcome! If you find a bug or have a suggestion for improvement, please open an issue on the [GitHub repository](https://github.com/your-username/sql-prettifier).

## License

`sql-prettifier` is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

Please note that the placeholders like `your-username` in the URLs should be replaced with the actual username or organization name on GitHub.