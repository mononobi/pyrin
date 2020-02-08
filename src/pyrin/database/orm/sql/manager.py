# -*- coding: utf-8 -*-
"""
database orm sql manager module.
"""

import sqlparse

from sqlalchemy.sql.elements import TextClause
from sqlparse.sql import IdentifierList, Identifier, Function, Parenthesis
from sqlparse.tokens import Name, Punctuation, Wildcard

from pyrin.core.context import Manager


class DatabaseORMSQLManager(Manager):
    """
    database orm sql manager class.
    """

    def find_table_names(self, expression):
        """
        finds table names from a string or `TextClause` sql expression.

        :param Union[str, TextClause] expression: a string or `TextClause`
                                                  containing a sql expression.

        :returns: list[str]
        :rtype: list
        """

        sql = expression
        tables = []
        if isinstance(expression, TextClause):
            sql = expression.text

        if sql is None or len(sql) <= 0:
            return tables

        parsed_result = sqlparse.parse(sql)
        for statement in parsed_result:
            self._add_table_names(statement.tokens, tables)

        return tables

    def _add_table_names(self, tokens, tables):
        """
        adds table names from given tokens into given tables list.

        :param list[Token] tokens: list of tokens to find tables in them.
        :param list[str] tables: list of table names to add to it.
        """

        for token in tokens:
            if isinstance(token, (Identifier, Function)) and len(token.tokens) > 0:
                if token.tokens[0].ttype == Name and self._is_column_name(token) is False:
                    if token.tokens[0].value.lower() not in tables:
                        tables.append(token.tokens[0].value.lower())
            elif isinstance(token, (IdentifierList, Parenthesis)):
                self._add_table_names(token.tokens, tables)

    def _is_column_name(self, token):
        """
        gets a value indicating that given token represents a column.
        for example: `table.some_column` or `table_alias.some_column`.

        :param Token token: token to be checked.

        :rtype: bool
        """

        for token in token.tokens:
            if token.ttype in (Punctuation, Wildcard):
                return True

        return False
