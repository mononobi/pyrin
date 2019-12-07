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
from pyrin.database.orm.query.exceptions import DataCouldNotBeFetchedError


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

        :keyword Union[type, tuple[type]] limit: class type of the entities that this
                                                 query instance will work on. if the
                                                 query is working on multiple entities,
                                                 this value must be a tuple of all class
                                                 types of that entities.

                                                 for example: if you set
                                                 `entities=SomeEntity.id, AnotherEntity.name`
                                                 you should leave `limit=None` to skip validation
                                                 or you could set
                                                 `limit=(SomeEntity, AnotherEntity)`
                                                 this way validation succeeds, but if
                                                 you set `limit=SomeEntity`
                                                 then the query will not be executed
                                                 and an error would be raised.

        :raises DataCouldNotBeFetchedError: data could not be fetched error.
        """

        limit = options.get('limit', None)
        if limit is not None:
            self._prepare_validation(entities, limit)

        super(CoreQuery, self).__init__(entities, session)

    def _validate_limit(self, entities, limit):
        """
        validates the query for given entities based on provided limit.

        :param tuple entities: entities or columns that needed for query.

        :param Union[type, tuple[type]] limit: class type of the entities that this
                                               query instance will work on. if the
                                               query is working on multiple entities,
                                               this value must be a tuple of all class
                                               types of that entities.

        :raises DataCouldNotBeFetchedError: data could not be fetched error.
        """

        limit_classes = set(entity for entity in limit if inspect.isclass(entity)
                            and issubclass(entity, CoreEntity))

        requested_classes = set(entity for entity in entities if inspect.isclass(entity)
                                and issubclass(entity, CoreEntity))

        requested_classes_by_column = set(column.class_ for column in entities if
                                          isinstance(column, InstrumentedAttribute)
                                          and issubclass(getattr(column, 'class_', type),
                                                         CoreEntity))

        all_requested_classes = requested_classes.union(requested_classes_by_column)

        if not all_requested_classes <= limit_classes:
            raise DataCouldNotBeFetchedError(_('Requested data could not be fetched. '
                                               'Please revise the requested fields.'))

    def _prepare_validation(self, entities, limit):
        """
        prepares entities and limit and validates them if required.

        :param tuple entities: entities or columns that needed for query.

        :param Union[type, tuple[type]] limit: class type of the entities that this
                                               query instance will work on. if the
                                               query is working on multiple entities,
                                               this value must be a tuple of all class
                                               types of that entities.

        :raises DataCouldNotBeFetchedError: data could not be fetched error.
        """

        if limit is None or entities is None:
            return

        if not isinstance(limit, LIST_TYPES):
            limit = tuple(limit)

        if not isinstance(entities, LIST_TYPES):
            entities = tuple(entities)

        if len(limit) <= 0 or len(entities) <= 0:
            return

        self._validate_limit(entities, limit)
