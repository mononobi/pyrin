# -*- coding: utf-8 -*-
"""
database orm query base module.
"""

import inspect

from sqlalchemy.orm import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute

from pyrin.core.globals import LIST_TYPES
from pyrin.database.model.base import CoreEntity


class CoreQuery(Query):
    """
    application query class.
    this class extends sqlalchemy `Query` class.
    """

    def __init__(self, entities, session=None, **options):
        """
        initializes an instance of CoreQuery.

        :param tuple entities: list of entities or columns that needed for query.
        :param Session session: optional session object to bind this query to it.

        :keyword Union[type, tuple[type]] valid_entities: class type of the entities that this
                                                          query instance will work on. if the
                                                          query is working on multiple entities,
                                                          this value must be a tuple of all class
                                                          types of that entities.

                                                          for example:
                                                          if you set
                                                          `entities=SomeEntity.id,
                                                          AnotherEntity.name`
                                                          you should leave `valid_entities=None`
                                                          to skip validation or you could set
                                                          `valid_entities=(SomeEntity,
                                                          AnotherEntity)`
                                                          this way validation succeeds, but if
                                                          you set `valid_entities=SomeEntity`
                                                          then the query will not be executed
                                                           and an error would be raised.
        """

        valid_entities = options.get('valid_entities', None)
        if valid_entities is not None and not isinstance(valid_entities, LIST_TYPES):
            valid_entities = tuple(valid_entities)

        if entities is None or not isinstance(entities, LIST_TYPES):
            entities = tuple(entities)

        if valid_entities is not None:
            self._validate_entities(entities, valid_entities)

        super(CoreQuery, self).__init__(entities, session)

    def _validate_entities(self, entities, valid_entities):
        """
        validates the query for given entities based on provided valid entities.

        :param tuple entities: list of entities or columns that needed for query.

        :param Union[type, tuple[type]] valid_entities: class type of the entities that this
                                                        query instance will work on. if the
                                                        query is working on multiple entities,
                                                        this value must be a tuple of all class
                                                        types of that entities.

        :raises
        """

        valid_classes = set(entity for entity in valid_entities if inspect.isclass(entity)
                            and issubclass(entity, CoreEntity))

        requested_classes = set(entity for entity in entities if inspect.isclass(entity)
                                and issubclass(entity, CoreEntity))

        requested_classes_by_column = set(column.class_ for column in entities if
                                          isinstance(column, InstrumentedAttribute)
                                          and issubclass(getattr(column, 'class_', type),
                                                         CoreEntity))

        all_requested_classes = requested_classes.union(requested_classes_by_column)

        if all_requested_classes > valid_classes:
            raise
