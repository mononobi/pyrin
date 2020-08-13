# -*- coding: utf-8 -*-
"""
orm sql extractor manager module.
"""

import sqlparse

from sqlalchemy.sql.elements import TextClause
from sqlparse.tokens import DML, Keyword
from sqlparse.sql import IdentifierList, Identifier, Function, Where, Comparison, TokenList

import pyrin.utils.misc as misc_utils

from pyrin.core.structs import Manager
from pyrin.database.orm.sql.extractor import ORMSQLExtractorPackage


class ORMSQLExtractorManager(Manager):
    """
    orm sql extractor manager class.
    """

    package_class = ORMSQLExtractorPackage

    def find_table_names(self, expression, **options):
        """
        finds table names from a string or `TextClause` sql expression.

        :param str | TextClause expression: a string or `TextClause`
                                            containing a sql expression.

        :keyword bool include_select: specifies that select statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :keyword bool include_insert: specifies that insert statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :keyword bool include_update: specifies that update statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :keyword bool include_delete: specifies that delete statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :rtype: list[str]
        """

        sql = expression
        tables = []
        if isinstance(expression, TextClause):
            sql = expression.text

        if sql is None or len(sql) <= 0:
            return tables

        return self._extract_tables(sql, **options)

    def _is_subselect(self, statement):
        """
        gets a value indicating that given statement is a select or sub-select.

        :param Statement statement: Statement object.

        :rtype: bool
        """

        if not statement.is_group:
            return False
        for item in statement.tokens:
            if item.ttype is DML and item.value.upper() == 'SELECT':
                return True
        return False

    def _is_insert(self, statement):
        """
        gets a value indicating that given statement is an insert.

        :param Statement statement: Statement object.

        :rtype: bool
        """

        if not statement.is_group:
            return False
        for item in statement.tokens:
            if item.ttype is DML and item.value.upper() == 'INSERT':
                return True
        return False

    def _is_update(self, statement):
        """
        gets a value indicating that given statement is an update.

        :param Statement statement: Statement object.

        :rtype: bool
        """

        if not statement.is_group:
            return False
        for item in statement.tokens:
            if item.ttype is DML and item.value.upper() == 'UPDATE':
                return True
        return False

    def _is_delete(self, statement):
        """
        gets a value indicating that given statement is a delete.

        :param Statement statement: Statement object.

        :rtype: bool
        """

        if not statement.is_group:
            return False
        for item in statement.tokens:
            if item.ttype is DML and item.value.upper() == 'DELETE':
                return True
        return False

    def _is_join(self, token):
        """
        gets a value indicating that given token represents a join keyword.

        :param Token token: token to be checked for join.

        :rtype: bool
        """

        if token.ttype is Keyword and (token.value.upper() == 'JOIN' or
                                       ' JOIN' in token.value.upper() or
                                       token.value.upper() == 'ON'):
            return True

        return False

    def _is_where(self, token):
        """
        gets a value indicating that given token represents a where clause.

        :param Token token: token to be checked for where clause.

        :rtype: bool
        """

        return isinstance(token, Where)

    def _is_comparison(self, token):
        """
        gets a value indicating that given token represents a comparison clause.

        :param Token token: token to be checked for comparison clause.

        :rtype: bool
        """

        return isinstance(token, Comparison)

    def _is_table(self, token):
        """
        gets a value indicating that given token represents a table.

        :param Token token: token to be checked for being table.

        :rtype: bool
        """

        return not self._is_join(token) and not self._is_where(token) and \
            not self._is_comparison(token)

    def _extract_select_from_part(self, statement):
        """
        extracts table names from a select statement.

        it also supports multiple joins and sub-selects.

        :param Statement statement: statement object.

        :rtype: list[Identifier]
        """

        select_seen = False
        from_seen = False
        join_seen = False
        results = []
        for item in statement.tokens:
            if item.is_group:
                for x in self._extract_select_from_part(item):
                    results.append(self._get_identifier(x, True))
            if select_seen is True and from_seen is True and join_seen is False:
                if self._is_subselect(item):
                    for z in self._extract_select_from_part(item):
                        results.append(self._get_identifier(z, True))
                elif item.ttype is Keyword and item.value.upper() in ['ORDER BY',
                                                                      'GROUP BY',
                                                                      'HAVING']:
                    return results
                elif self._is_join(item) is True:
                    join_seen = True
                elif item.value not in (None, '') and not item.value.isspace() and \
                        self._is_table(item) is True:
                    results.append(self._get_identifier(item, True))
            elif select_seen is True and from_seen is True and join_seen is True:
                if item.value not in (None, '') and not item.value.isspace() and \
                        self._is_table(item) is True:
                    results.append(self._get_identifier(item, True))
            elif item.ttype is Keyword.DML and item.value.upper() == 'SELECT':
                select_seen = True
            elif item.ttype is Keyword and item.value.upper() == 'FROM':
                from_seen = True
            elif self._is_join(item) is True:
                join_seen = True

        return results

    def _extract_insert_into_part(self, statement):
        """
        extracts table name from an insert statement.

        :param Statement statement: statement object.

        :rtype: Identifier
        """

        insert_seen = False
        into_seen = False
        for item in statement.tokens:
            if insert_seen is True and into_seen is True:
                if item.value not in (None, '') and not item.value.isspace() and \
                        self._is_table(item) is True:
                    return self._get_identifier(item, True)
            elif item.ttype is Keyword.DML and item.value.upper() == 'INSERT':
                insert_seen = True
            elif item.ttype is Keyword and item.value.upper() == 'INTO':
                into_seen = True

        return None

    def _extract_update_part(self, statement):
        """
        extracts table name from an update statement.

        :param Statement statement: statement object.

        :rtype: Identifier
        """

        update_seen = False
        for item in statement.tokens:
            if update_seen is True:
                if item.value not in (None, '') and not item.value.isspace() and \
                        self._is_table(item) is True:
                    return self._get_identifier(item, True)
            elif item.ttype is Keyword.DML and item.value.upper() == 'UPDATE':
                update_seen = True

        return None

    def _extract_delete_from_part(self, statement):
        """
        extracts table name from a delete statement.

        :param Statement statement: statement object.

        :rtype: Identifier
        """

        delete_seen = False
        from_seen = False
        for item in statement.tokens:
            if delete_seen is True and from_seen is True:
                if item.value not in (None, '') and not item.value.isspace() and \
                        self._is_table(item) is True:
                    return self._get_identifier(item, True)
            elif item.ttype is Keyword.DML and item.value.upper() == 'DELETE':
                delete_seen = True
            elif item.ttype is Keyword and item.value.upper() == 'FROM':
                from_seen = True

        return None

    def _extract_table_identifiers(self, token_stream):
        """
        extracts all potential table names from input single or collection `TokenList`.

        :param list[TokenList] | TokenList token_stream: a single `TokenList` or
                                                         collection of `TokenList`
                                                         objects to be checked.

        :rtype: list[str]
        """

        result = []
        if token_stream is not None:
            token_stream = misc_utils.make_iterable(token_stream, list)
            for item in token_stream:
                if item is not None:
                    if isinstance(item, IdentifierList):
                        for identifier in item.get_identifiers():
                            if isinstance(identifier, TokenList):
                                if identifier.get_real_name().lower() not in result:
                                    result.append(identifier.get_real_name().lower())
                            else:
                                if identifier.value.lower() not in result:
                                    result.append(identifier.value.lower())
                    elif isinstance(item, Identifier):
                        if item.get_real_name().lower() not in result:
                            result.append(item.get_real_name().lower())
                    elif item.ttype is Keyword:
                        if item.value not in result:
                            result.append(item.value.lower())
                    elif isinstance(item, Function):
                        if item.value not in result:
                            result.append(item.value.lower())

        return result

    def _extract_tables(self, sql, **options):
        """
        extracts all tables from given sql string expression.
        tables will be ordered as they appeared in input expression.

        :param str sql: sql expression be extracted for table names.

        :keyword bool include_select: specifies that select statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :keyword bool include_insert: specifies that insert statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :keyword bool include_update: specifies that update statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :keyword bool include_delete: specifies that delete statements
                                      must be investigated for table names.
                                      defaults to True if not provided.

        :rtype: list[str]
        """

        include_select = options.get('include_select', True)
        include_insert = options.get('include_insert', True)
        include_update = options.get('include_update', True)
        include_delete = options.get('include_delete', True)

        extracted_tables = {}
        statements = sqlparse.parse(sql)
        for statement in statements:
            stream = None
            if statement.get_type() != 'UNKNOWN':
                if include_select is True and self._is_subselect(statement):
                    stream = self._extract_select_from_part(statement)
                    extracted_tables.update(**dict.fromkeys(
                        self._extract_table_identifiers(stream), None))
                if include_insert is True and self._is_insert(statement):
                    stream = self._extract_insert_into_part(statement)
                    extracted_tables.update(**dict.fromkeys(
                        self._extract_table_identifiers(stream), None))
                if include_update is True and self._is_update(statement):
                    stream = self._extract_update_part(statement)
                    extracted_tables.update(**dict.fromkeys(
                        self._extract_table_identifiers(stream), None))
                if include_delete is True and self._is_delete(statement):
                    stream = self._extract_delete_from_part(statement)
                    extracted_tables.update(**dict.fromkeys(
                        self._extract_table_identifiers(stream), None))

        return list(extracted_tables.keys())

    def _get_identifier(self, token, force=False):
        """
        gets the identifier token available in given tokens children.

        :param Token | TokenList token: token to get its child identifier.

        :param bool force: specifies that if its child is not an
                           `Identifier` but it is a keyword, return it.
                           it could be helpful for some situations which
                           table names are equal to some keywords.

        :rtype: Identifier | Keyword
        """

        if token is not None:
            if isinstance(token, (Identifier, IdentifierList)):
                return token

            elif isinstance(token, Function) and force is True:
                return token.tokens[0]

            elif token.ttype is Keyword and force is True:
                return token

        return None
