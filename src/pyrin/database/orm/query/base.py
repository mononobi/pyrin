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

        :keyword Union[type, tuple[type]] bound: class type of the entities that this
                                                 query instance will work on. if the
                                                 query is working on multiple entities,
                                                 this value must be a tuple of all class
                                                 types of that entities.

                                                 for example: if you set
                                                 `entities=SomeEntity.id, AnotherEntity.name`
                                                 you should leave `bound=None` to skip validation
                                                 or you could set
                                                 `bound=(SomeEntity, AnotherEntity)`
                                                 this way validation succeeds, but if
                                                 you set `bound=SomeEntity`
                                                 then the query will not be executed
                                                 and an error would be raised.

        :raises DataCouldNotBeFetchedError: data could not be fetched error.
        """

        bound = options.get('bound', None)
        if bound is not None:
            self._prepare_validation(entities, bound)

        super(CoreQuery, self).__init__(entities, session)

    def _validate_bound(self, entities, bound):
        """
        validates the query for given entities based on provided bound.

        :param tuple entities: entities or columns that needed for query.

        :param Union[type, tuple[type]] bound: class type of the entities that this
                                               query instance will work on. if the
                                               query is working on multiple entities,
                                               this value must be a tuple of all class
                                               types of that entities.

        :raises DataCouldNotBeFetchedError: data could not be fetched error.
        """

        bound_classes = set(entity for entity in bound if inspect.isclass(entity)
                            and issubclass(entity, CoreEntity))

        requested_classes = set(entity for entity in entities if inspect.isclass(entity)
                                and issubclass(entity, CoreEntity))

        requested_classes_by_column = set(column.class_ for column in entities if
                                          isinstance(column, InstrumentedAttribute)
                                          and issubclass(getattr(column, 'class_', type),
                                                         CoreEntity))

        all_requested_classes = requested_classes.union(requested_classes_by_column)

        if not all_requested_classes.issubset(bound_classes):
            raise DataCouldNotBeFetchedError(_('Requested data could not be fetched. '
                                               'Please revise the requested fields.'))

    def _prepare_validation(self, entities, bound):
        """
        prepares entities and bound and validates them if required.

        :param tuple entities: entities or columns that needed for query.

        :param Union[type, tuple[type]] bound: class type of the entities that this
                                               query instance will work on. if the
                                               query is working on multiple entities,
                                               this value must be a tuple of all class
                                               types of that entities.

        :raises DataCouldNotBeFetchedError: data could not be fetched error.
        """

        if bound is None or entities is None:
            return

        if not isinstance(bound, LIST_TYPES):
            bound = tuple(bound)

        if not isinstance(entities, LIST_TYPES):
            entities = tuple(entities)

        if len(bound) <= 0 or len(entities) <= 0:
            return

        self._validate_bound(entities, bound)
