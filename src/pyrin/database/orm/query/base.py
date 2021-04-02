# -*- coding: utf-8 -*-
"""
orm query base module.
"""

import inspect

from sqlalchemy.orm import Query, lazyload
from sqlalchemy import inspection, log, func, literal, distinct, select
from sqlalchemy.orm.attributes import InstrumentedAttribute

import pyrin.utils.misc as misc_utils
import pyrin.utils.sqlalchemy as sqlalchemy_utils
import pyrin.database.paging.services as paging_services
import pyrin.security.session.services as session_services

from pyrin.core.globals import _, SECURE_FALSE, SECURE_TRUE
from pyrin.database.model.base import BaseEntity
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.services import get_current_store
from pyrin.database.orm.query.exceptions import ColumnsOutOfScopeError, \
    InvalidOrderByScopeError, EfficientCountIsNotPossibleError


@inspection._self_inspects
@log.class_logger
class CoreQuery(Query):
    """
    core query class.

    this is the application default query class.
    it extends sqlalchemy `Query` class.
    """

    def __init__(self, entities, session=None, **options):
        """
        initializes an instance of CoreQuery.

        this method has been overridden to provide the concept of scope to queries.
        it is useful if you want to let users (end users not developers) to select
        which columns they want to be returned in a service. in this situation, if
        there is no scope defined, they could add any columns of other entities, but
        using scope, prevents this. but on normal use cases there is no need to define
        scope, and its also more efficient.

        :param tuple entities: entities or columns that are needed for query.
        :param Session session: optional session object to bind this query to it.

        :keyword type | tuple[type] scope: class type of the entities that this
                                           query instance will work on. if the
                                           query is working on multiple entities,
                                           this value must be a tuple of all class
                                           types of that entities.

                                           for example: if you set
                                           `entities=SomeEntity.id, AnotherEntity.name`
                                           you should leave `scope=None` to skip validation
                                           or you could set
                                           `scope=(SomeEntity, AnotherEntity)`
                                           this way validation succeeds, but if
                                           you set `scope=SomeEntity`
                                           then the query will not be executed
                                           and an error will be raised.

        :raises ColumnsOutOfScopeError: columns out of scope error.
        """

        scope = options.get('scope', None)
        if scope is not None:
            self._prepare_validation(entities, scope)

        super().__init__(entities, session)

    def _validate_scope(self, entities, scope):
        """
        validates the query for given entities based on provided scope.

        :param tuple entities: entities or columns that needed for query.

        :param type[BaseEntity] | tuple[type[BaseEntity]] scope: class type of the entities
                                                                 that this query instance will
                                                                 work on. if the query is working
                                                                 on multiple entities, this value
                                                                 must be a tuple of all class
                                                                 types of that entities.

        :raises ColumnsOutOfScopeError: columns out of scope error.
        """

        scope_classes = set(entity for entity in scope if inspect.isclass(entity)
                            and issubclass(entity, BaseEntity))

        requested_classes = set(entity for entity in entities if inspect.isclass(entity)
                                and issubclass(entity, BaseEntity))

        requested_classes_by_column = set(column.class_ for column in entities if
                                          isinstance(column, InstrumentedAttribute)
                                          and issubclass(getattr(column, 'class_', type),
                                                         BaseEntity))

        all_requested_classes = requested_classes.union(requested_classes_by_column)

        if not all_requested_classes.issubset(scope_classes):
            raise ColumnsOutOfScopeError(_('Requested columns are out of scope of this '
                                           'query. Please revise the requested columns.'))

    def _prepare_validation(self, entities, scope):
        """
        prepares entities and scope and validates them if required.

        :param tuple entities: entities or columns that needed for query.

        :param type[BaseEntity] | tuple[type[BaseEntity]] scope: class type of the entities that
                                                                 this query instance will work on.
                                                                 if the query is working on
                                                                 multiple entities, this value
                                                                 must be a tuple of all class
                                                                 types of that entities.

        :raises ColumnsOutOfScopeError: columns out of scope error.
        """

        if scope is None or entities is None:
            return

        scope = misc_utils.make_iterable(scope, tuple)
        entities = misc_utils.make_iterable(entities, tuple)

        if len(scope) <= 0 or len(entities) <= 0:
            return

        self._validate_scope(entities, scope)

    def _copy_statement(self, old_statement, *new_columns):
        """
        gets a copy of given statement with columns replaced with new columns.

        this method is used to generate statement for `_count` function.

        :param Select old_statement: the original statement to make a copy of it.
        :param CoreColumn | str new_columns: new columns to be used in copied statement.

        :rtype: Select
        """

        statement = select(*new_columns).select_from(*old_statement.froms)
        statement._where_criteria = old_statement._where_criteria
        statement._group_by_clauses = old_statement._group_by_clauses
        statement._having_criteria = old_statement._having_criteria
        statement._distinct_on = old_statement._distinct_on
        statement._distinct = old_statement._distinct
        statement._limit_clause = old_statement._limit_clause
        statement._offset_clause = old_statement._offset_clause
        statement._order_by_clauses = old_statement._order_by_clauses
        statement._correlate = old_statement._correlate
        statement._correlate_except = old_statement._correlate_except
        statement._auto_correlate = old_statement._auto_correlate

        return statement

    def _get_appropriate_column(self, *columns):
        """
        gets the appropriate column to be used in `_count` function.

        it may return None if no appropriate column could be found.

        :param CoreColumn | object columns: columns to choose from.

        :rtype: CoreColumn | str
        """

        if columns is None or len(columns) <= 0 or columns[0] is None:
            return None

        if len(columns) == 1:
            return columns[0]

        for item in columns:
            if not isinstance(item, CoreColumn):
                return None

        return '*'

    def _count(self, **options):
        """
        returns the count of rows that the sql formed by this `Query` would return.

        this method generates a single sql query like below:
        select count(column, ...)
        from table
        where ...

        if a single query could not be produced, an error may be raised.

        :keyword CoreColumn column: column to be used in count function.
                                    defaults to `*` if not provided.

        :keyword bool distinct: specifies that count should
                                be executed on distinct select.
                                defaults to False if not provided.
                                note that `distinct` will only be
                                used if `column` is also provided.

        :raises EfficientCountIsNotPossibleError: efficient count is not possible error.

        :rtype: int
        """

        old_statement = self.options(lazyload('*')).statement
        if not old_statement.is_select or not old_statement.is_selectable:
            raise EfficientCountIsNotPossibleError('The provided statement is not a select '
                                                   'statement and efficient count could not '
                                                   'be produced for it.')

        if old_statement._group_by_clauses is not None \
                and len(old_statement._group_by_clauses) > 0:
            raise EfficientCountIsNotPossibleError('The provided statement has group by clause '
                                                   'and efficient count could not be produced '
                                                   'for it.')

        column = options.get('column')
        is_distinct = options.get('distinct', False)
        func_count = None
        if column is None:
            column = self._get_appropriate_column(*old_statement.selected_columns)
            if column is None:
                raise EfficientCountIsNotPossibleError('The provided statement has complex '
                                                       'columns and efficient count could not '
                                                       'be produced for it.')
            func_count = func.count(column)
        else:
            if is_distinct is True:
                func_count = func.count(distinct(column))
            else:
                func_count = func.count(column)

        statement = self._copy_statement(old_statement, func_count).order_by(None)
        store = get_current_store()
        result = store.execute(statement).scalar()
        if result is None:
            result = 0

        return result

    def count(self, **options):
        """
        returns the count of rows that the sql formed by this `Query` would return.

        this method is overridden to prevent inefficient count() of sqlalchemy `Query`
        which produces a subquery, if possible. otherwise it uses the default sqlalchemy
        `count` method.

        :keyword CoreColumn column: column to be used in count function.
                                    defaults to `*` if not provided.
                                    this is only used if a single query
                                    could be produced for count.

        :keyword bool distinct: specifies that count should
                                be executed on distinct select.
                                defaults to False if not provided.
                                note that `distinct` will only be
                                used if `column` is also provided.

        :rtype: int
        """

        try:
            return self._count(**options)
        except Exception:
            return super().count()

    def paginate(self, **options):
        """
        sets the offset and limit for current query.

        the offset and limit values will be extracted from given inputs.
        note that `.paginate` must be called after all other query methods
        have been called. otherwise unexpected behaviour may occur.

        if there is no request context available or there is no paginator for
        current request, pagination will be ignored. this is required to prevent
        security risks by clients.

        if you want pagination outside of request context, you could use
        `.limit` and `.offset` methods directly.

        :keyword SECURE_TRUE | SECURE_FALSE inject_total: inject total count into
                                                          current request.
                                                          defaults to `SECURE_FALSE`
                                                          if not provided.

        :keyword CoreColumn column: column to be used in count function.
                                    defaults to `*` if not provided.
                                    this is only used if `inject_total` is
                                    provided and a single query could be
                                    produced for count.

        :keyword bool distinct: specifies that count should
                                be executed on distinct select.
                                defaults to False if not provided.
                                note that `distinct` will only be
                                used if `column` is also provided.

        :keyword int __limit__: limit value.
        :keyword int __offset__: offset value.
        """

        inject_total = options.get('inject_total', SECURE_FALSE)
        paginator = None
        if session_services.is_request_context_available() is True:
            paginator = session_services.get_request_context('paginator', None)
        else:
            return self

        if paginator is not None:
            if inject_total is SECURE_TRUE:
                paginator.total_count = self.order_by(None).count(**options)

            limit, offset = paging_services.get_paging_keys(**options)
            return self.limit(limit).offset(offset)

        return self

    def existed(self):
        """
        gets a value indicating that current query has any results.

        this is a helper method to simplify the use of `.exists` method of sqlalchemy.

        :rtype: bool
        """

        store = get_current_store()
        result = store.query(literal(True)).filter(self.exists()).scalar()
        return result is True

    def delete(self, synchronize_session=False):
        """
        performs a bulk delete query.

        this method is overridden to provide the most performant
        `synchronize_session` value as default value.

        :param str | bool synchronize_session: session synchronization strategy.
                                               it could be set to False, `fetch`
                                               or `evaluate`. defaults to False.

        :returns: count of affected rows
        :rtype: int
        """

        return super().delete(synchronize_session=synchronize_session)

    def update(self, values, synchronize_session=False, update_args=None):
        """
        performs a bulk update query.

        this method is overridden to provide the most performant
        `synchronize_session` value as default value.

        :param values: a dictionary with attributes names, or alternatively
                       mapped attributes or sql expressions, as keys, and
                       literal values or sql expressions as values.

        :param str | bool synchronize_session: session synchronization strategy.
                                               it could be set to False, `fetch`
                                               or `evaluate`. defaults to False.

        :param update_args: optional dictionary, if present will be passed
                            to the underlying `_expression.update` construct
                            as the `**kw` for the object.

        :returns: count of affected rows
        :rtype: int
        """

        return super().update(values,
                              synchronize_session=synchronize_session,
                              update_args=update_args)

    def safe_order_by(self, scope, *force_order, **options):
        """
        apply one or more `ORDER BY` criterion to the query and return new `CoreQuery`.

        this method only accepts column names, not instances.
        it is implemented to be used for ordering by client inputs.

        this method will automatically fetch order by columns from `order_by`
        keyword if it is provided in options.

        default ordering is ascending, but it could be changed to descending
        by prefixing `-` to column names.

        for example:

        name, +age -> ordering for name and age columns both ascending.
        name, -age -> ordering for name ascending and age descending.

        if column names are not valid, this method ignores them and does not produce
        invalid order by expression. if you do not want to ignore invalid columns,
        use `order_by` method instead.

        :param type[BaseEntity] | list[str] scope: entity class or a list of column names
                                                   to pick order by columns from it.
                                                   note that if a list is provided, column
                                                   names must be the name of actual table
                                                   columns.

        :param str force_order: column names to be appended to `order_by` columns.
                                note that they must be the attribute names
                                of entity if scope is an entity class, otherwise
                                they must be the actual table column names.

        :keyword list[str] | str order_by: column names to be used in order by criterion.
                                           this value is defined to let clients directly
                                           provide order by columns to services through
                                           options. if `order_by` is provided, and
                                           `force_order` is also provided, `force_order`
                                           will be appended to `order_by` values.
                                           it is useful if you want to assure that always
                                           a valid order by will be generated even if
                                           client does not provide any column names.
                                           note that column names must be the attribute names
                                           of entity if scope is an entity class, otherwise
                                           they must be the actual table column names.

        :raises InvalidOrderByScopeError: invalid order by scope error.

        :rtype: CoreQuery
        """

        criterion = None
        columns = options.get('order_by')
        columns = misc_utils.make_iterable(columns, list)
        columns.extend(force_order)

        if isinstance(scope, type) and issubclass(scope, BaseEntity):
            criterion = scope.get_ordering_criterion(*columns, ignore_invalid=True)

        elif isinstance(scope, list):
            criterion = sqlalchemy_utils.get_ordering_criterion(*columns,
                                                                valid_columns=scope,
                                                                ignore_invalid=True)
        else:
            raise InvalidOrderByScopeError('Order by "scope" must be an entity '
                                           'class or a list of column names.')

        return self.order_by(*criterion)
