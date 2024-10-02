import sqlparse
from sqlparse.tokens import (
    Keyword, Name, Punctuation, Whitespace, Newline, String, Number, Comment, Operator
)
from sqlparse.sql import (
    IdentifierList, Identifier, Where, Function, Parenthesis, Comparison, Token, Case
)


class SqlFormatter:
    def __init__(self,
                 keyword_case='upper',
                 identifier_case='preserve',
                 comma='leading',
                 use_as_column_aliases=True,
                 use_as_table_aliases=False,
                 indent_style='space',
                 indent_size=4,
                 line_breaks_before_clauses=False,
                 line_breaks_after_clauses=True,
                 align_keywords=False,
                 space_around_operators=True,
                 parentheses_style='standard',
                 newline_after_each_column=False,
                 uppercase_functions=False,
                 space_after_function_name=False,
                 dialect='generic',
                 quote_identifiers='none',
                 wrap_after=80,
                 compact=False,
                 semicolon_newline=False,
                 comment_style='preserve',
                 boolean_literal_case='upper',
                 join_indentation='indent',
                 subquery_style='indent',
                 case_when_indentation='standard',
                 space_inside_parentheses=False,
                 uppercase_datatypes=False,
                 split_statements=False,
                 select_clause_newline=False,
                 align_operators=False,
                 alias_in_select='as',
                 string_quotes='single',
                 empty_lines_between_clauses=False,
                 set_operation_indentation='align',
                 keyword_alignment='left',
                 conditional_expression_style='inline',
                 inline_comments_position='same_line',
                 block_comment_style='preserve',
                 collection_datatype_formatting='standard',
                 limit_clause_position='same_line'):
        self.keyword_case = keyword_case.lower()
        self.identifier_case = identifier_case.lower()
        self.comma = comma.lower()
        self.use_as_column_aliases = use_as_column_aliases
        self.use_as_table_aliases = use_as_table_aliases
        self.indent_style = indent_style
        self.indent_size = indent_size
        self.line_breaks_before_clauses = line_breaks_before_clauses
        self.line_breaks_after_clauses = line_breaks_after_clauses
        self.align_keywords = align_keywords
        self.space_around_operators = space_around_operators
        self.parentheses_style = parentheses_style
        self.newline_after_each_column = newline_after_each_column
        self.uppercase_functions = uppercase_functions
        self.space_after_function_name = space_after_function_name
        self.dialect = dialect
        self.quote_identifiers = quote_identifiers
        self.wrap_after = wrap_after
        self.compact = compact
        self.semicolon_newline = semicolon_newline
        self.comment_style = comment_style
        self.boolean_literal_case = boolean_literal_case
        self.join_indentation = join_indentation
        self.subquery_style = subquery_style
        self.case_when_indentation = case_when_indentation
        self.space_inside_parentheses = space_inside_parentheses
        self.uppercase_datatypes = uppercase_datatypes
        self.split_statements = split_statements
        self.select_clause_newline = select_clause_newline
        self.align_operators = align_operators
        self.alias_in_select = alias_in_select
        self.string_quotes = string_quotes
        self.empty_lines_between_clauses = empty_lines_between_clauses
        self.set_operation_indentation = set_operation_indentation
        self.keyword_alignment = keyword_alignment
        self.conditional_expression_style = conditional_expression_style
        self.inline_comments_position = inline_comments_position
        self.block_comment_style = block_comment_style
        self.collection_datatype_formatting = collection_datatype_formatting
        self.limit_clause_position = limit_clause_position

        # Internal state
        self.current_indent = 0
        self.indent_char = '\t' if self.indent_style == 'tab' else ' ' * self.indent_size

    def format(self, sql_string):
        if self.split_statements:
            statements = sqlparse.split(sql_string)
        else:
            statements = [sql_string]

        formatted_sql = []
        for stmt in statements:
            parsed = sqlparse.parse(stmt)[0]
            formatted_statement = self._format_statement(parsed)
            formatted_sql.append(formatted_statement)

        result = '\n'.join(formatted_sql)
        return result

    def _format_statement(self, statement):
        result = []
        for token in statement.tokens:
            formatted_token = self._format_token(token)
            result.append(formatted_token)
        return ''.join(result)

    def _format_token(self, token):
        if token.is_whitespace:
            return ' ' if not self.compact else ''
        elif token.ttype in Comment:
            return self._format_comment(token)
        elif token.ttype in Keyword:
            return self._format_keyword(token)
        elif isinstance(token, IdentifierList):
            return self._format_identifier_list(token)
        elif isinstance(token, Identifier):
            return self._format_identifier(token)
        elif isinstance(token, Function):
            return self._format_function(token)
        elif isinstance(token, Where):
            return self._format_where(token)
        elif isinstance(token, Parenthesis):
            return self._format_parenthesis(token)
        elif isinstance(token, Comparison):
            return self._format_comparison(token)
        elif isinstance(token, Case):
            return self._format_case(token)
        elif token.ttype in (String.Symbol, String.Single, String.Double):
            return self._format_string(token)
        elif token.ttype in Number:
            return self._format_number(token)
        elif token.ttype in Operator:
            return self._format_operator(token)
        else:
            return str(token)

    def _format_comment(self, token):
        # Handle comment formatting based on comment_style
        value = str(token)
        if self.comment_style == 'preserve':
            return value
        elif self.comment_style == 'uppercase':
            return value.upper()
        elif self.comment_style == 'lowercase':
            return value.lower()
        elif self.comment_style == 'capitalize':
            return value.capitalize()
        else:
            return value

    def _format_keyword(self, token):
        value = token.value.upper() if self.keyword_case == 'upper' else \
                token.value.lower() if self.keyword_case == 'lower' else \
                token.value.capitalize() if self.keyword_case == 'capitalize' else token.value

        if self.line_breaks_before_clauses and token.value.upper() in ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT']:
            value = '\n' + self._get_indent() + value
        elif self.line_breaks_after_clauses and token.value.upper() in ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT']:
            value = value + '\n' + self._get_indent()

        return value

    def _format_identifier_list(self, token):
        identifiers = []
        for idx, identifier in enumerate(token.get_identifiers()):
            formatted_identifier = self._format_identifier(identifier)
            if idx < len(list(token.get_identifiers())) - 1:
                if self.comma == 'trailing':
                    formatted_identifier += ','
                elif self.comma == 'leading':
                    formatted_identifier = ',' + formatted_identifier
            identifiers.append(formatted_identifier)
        separator = '\n' + self._get_indent() if self.newline_after_each_column else ' '
        return separator.join(identifiers)

    def _format_identifier(self, token):
        value = token.get_real_name()
        if self.identifier_case == 'upper':
            value = value.upper()
        elif self.identifier_case == 'lower':
            value = value.lower()
        elif self.identifier_case == 'capitalize':
            value = value.capitalize()

        alias = token.get_alias()
        if alias:
            if self.alias_in_select == 'as':
                alias_str = ' AS ' + alias
            elif self.alias_in_select == 'space':
                alias_str = ' ' + alias
            else:
                alias_str = ''
            value += alias_str

        return value

    def _format_function(self, token):
        fname = token.get_name()
        if self.uppercase_functions:
            fname = fname.upper()

        if self.space_after_function_name:
            fname += ' '

        args = ''.join([self._format_token(t) for t in token.get_parameters()])

        if self.space_inside_parentheses:
            return f"{fname}( {args} )"
        else:
            return f"{fname}({args})"

    def _format_where(self, token):
        self.current_indent += 1
        formatted = 'WHERE ' + ''.join([self._format_token(t) for t in token.tokens[1:]])
        self.current_indent -= 1
        return formatted

    def _format_parenthesis(self, token):
        content = ''.join([self._format_token(t) for t in token.tokens[1:-1]])
        if self.parentheses_style == 'break':
            indent = self._get_indent()
            self.current_indent += 1
            content = '\n' + indent + content + '\n' + indent
            self.current_indent -= 1
            return '(' + content + ')'
        else:
            if self.space_inside_parentheses:
                return f"( {content} )"
            else:
                return f"({content})"

    def _format_comparison(self, token):
        left = self._format_token(token.left)
        right = self._format_token(token.right)
        operator = str(token.tokens[1])
        if self.space_around_operators:
            return f"{left} {operator} {right}"
        else:
            return f"{left}{operator}{right}"

    def _format_case(self, token):
        # Simplified implementation
        result = 'CASE'
        for t in token.tokens[1:]:
            result += ' ' + self._format_token(t)
        return result

    def _format_string(self, token):
        value = str(token)
        if self.string_quotes == 'double':
            value = value.replace("'", '"')
        elif self.string_quotes == 'single':
            value = value.replace('"', "'")
        return value

    def _format_number(self, token):
        value = str(token)
        # Handle number_format and boolean_literal_case if needed
        return value

    def _format_operator(self, token):
        value = str(token)
        if self.space_around_operators:
            return ' ' + value + ' '
        else:
            return value

    def _get_indent(self):
        return self.indent_char * self.current_indent