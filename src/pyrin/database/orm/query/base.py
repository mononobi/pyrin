# -*- coding: utf-8 -*-
"""
database orm query base module.
"""

import inspect

from sqlalchemy import inspection, log
from sqlalchemy.orm import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute

from pyrin.core.globals import LIST_TYPES, _
from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.query.exceptions import ColumnsOutOfScopeError


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

        :param tuple entities: entities or columns that are needed for query.
        :param Session session: optional session object to bind this query to it.

        :keyword Union[type, tuple[type]] scope: class type of the entities that this
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
                                                 and an error would be raised.

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

        :param Union[type, tuple[type]] scope: class type of the entities that this
                                               query instance will work on. if the
                                               query is working on multiple entities,
                                               this value must be a tuple of all class
                                               types of that entities.

        :raises ColumnsOutOfScopeError: columns out of scope error.
        """

        scope_classes = set(entity for entity in scope if inspect.isclass(entity)
                            and issubclass(entity, CoreEntity))

        requested_classes = set(entity for entity in entities if inspect.isclass(entity)
                                and issubclass(entity, CoreEntity))

        requested_classes_by_column = set(column.class_ for column in entities if
                                          isinstance(column, InstrumentedAttribute)
                                          and issubclass(getattr(column, 'class_', type),
                                                         CoreEntity))

        all_requested_classes = requested_classes.union(requested_classes_by_column)

        if not all_requested_classes.issubset(scope_classes):
            raise ColumnsOutOfScopeError(_('Requested columns are out of scope of this '
                                           'query. Please revise the requested columns.'))

    def _prepare_validation(self, entities, scope):
        """
        prepares entities and scope and validates them if required.

        :param tuple entities: entities or columns that needed for query.

        :param Union[type, tuple[type]] scope: class type of the entities that this
                                               query instance will work on. if the
                                               query is working on multiple entities,
                                               this value must be a tuple of all class
                                               types of that entities.

        :raises ColumnsOutOfScopeError: columns out of scope error.
        """

        if scope is None or entities is None:
            return

        if not isinstance(scope, LIST_TYPES):
            scope = (scope,)

        if not isinstance(entities, LIST_TYPES):
            entities = (entities,)

        if len(scope) <= 0 or len(entities) <= 0:
            return

        self._validate_scope(entities, scope)
