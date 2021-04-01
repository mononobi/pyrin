# -*- coding: utf-8 -*-
"""
model base module.
"""

from pyrin.core.structs import CoreObject
from pyrin.core.decorators import class_property
from pyrin.database.model.mixin import CRUDMixin, MagicMethodMixin, QueryMixin, \
    ForeignKeyMixin, ColumnMixin, PrimaryKeyMixin, RelationshipMixin, \
    HybridPropertyMixin, ConverterMixin, AttributeMixin, MetadataMixin, \
    ModelCacheMixin, DefaultPrefetchMixin, OrderingMixin


class BaseEntity(MagicMethodMixin, PrimaryKeyMixin,
                 ForeignKeyMixin, ColumnMixin,
                 RelationshipMixin, HybridPropertyMixin,
                 AttributeMixin, CRUDMixin,
                 QueryMixin, ConverterMixin,
                 MetadataMixin, ModelCacheMixin,
                 DefaultPrefetchMixin, OrderingMixin,
                 CoreObject):
    """
    base entity class.

    it should be used as the base class for every declarative base class.
    for example `CoreEntity`, which by default is the application's declarative
    base class, inherits from this.

    if you want to implement a new declarative base class for your application models
    instead of `CoreEntity`, you must inherit your new base class from `BaseEntity`.
    because application will check isinstance() on this class's type to detect models.
    the new base class must be a `DeclarativeMeta`.
    note that your application must have a unique declarative base class for all
    models, do not mix the use of your new base class and `CoreEntity`, otherwise
    you will face problems in migrations and also multi-database environments.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of BaseEntity.

        note that this method will only be called on user code, meaning
        that results returned by orm from database will not call `__init__`
        of each entity.

        it could fill primary keys, foreign keys, other columns, hybrid properties
        and also relationship properties provided in keyword arguments.
        note that relationship values must be entities. this method could
        not convert relationships which are dict, into entities.

        :keyword SECURE_TRUE | SECURE_FALSE writable: specifies that any column which has
                                                      `allow_write=False` or its name starts
                                                      with underscore `_`, should not be
                                                      populated from given values. this
                                                      is useful if you want to fill an
                                                      entity with keyword arguments passed
                                                      from client and then doing the
                                                      validation. but do not want to expose
                                                      a security risk. especially in update
                                                      operations. defaults to `SECURE_TRUE`
                                                      if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_invalid_column: specifies that if a key is
                                                                   not available in entity
                                                                   columns, do not raise an
                                                                   error. defaults to
                                                                   `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_pk: specifies that any primary key column
                                                       should not be populated with given
                                                       values. this is useful if you want to
                                                       fill an entity with keyword arguments
                                                       passed from client and then doing the
                                                       validation. but do not want to let user
                                                       set primary keys and exposes a security
                                                       risk. especially in update operations.
                                                       defaults to `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_fk: specifies that any foreign key column
                                                       should not be populated with given
                                                       values. this is useful if you want
                                                       to fill an entity with keyword arguments
                                                       passed from client and then doing the
                                                       validation. but do not want to let user
                                                       set foreign keys and exposes a security
                                                       risk. especially in update operations.
                                                       defaults to `SECURE_FALSE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_relationships: specifies that any relationship
                                                                  property should not be populated
                                                                  with given values. defaults to
                                                                  `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE populate_all: specifies that all available values
                                                          must be populated from provided keyword
                                                          arguments. if set to `SECURE_TRUE`, all
                                                          other parameters will be bypassed.
                                                          this is for convenience of usage.
                                                          defaults to `SECURE_FALSE` if not
                                                          provided.

        :keyword SECURE_TRUE | SECURE_FALSE prefetch_complex_defaults: specifies that all columns
                                                                       that have default values
                                                                       for insert must fetch their
                                                                       default value if no value
                                                                       is provided for them in
                                                                       `kwargs`.
                                                                       note that scalar default
                                                                       values will always be
                                                                       fetched and this option is
                                                                       only for sequence or
                                                                       callable default values.
                                                                       defaults to `SECURE_TRUE`
                                                                       if not provided.

        :note prefetch_complex_defaults: for callable defaults we have to pass
                                         `ExecutionContext` as None because there is no
                                         such context in prefetch time. so if your callable
                                         default actually needs a valid context, you can not
                                         prefetch its value and must disable prefetching by
                                         passing `prefetch_complex_defaults=SECURE_FALSE`.
                                         otherwise unexpected behavior may occur.

        :raises ColumnNotExistedError: column not existed error.
        """

        super().__init__()

        self._set_name(self.__class__.__name__)
        self.from_dict(**kwargs)
        self.prefetch_insert_defaults(**kwargs)

    @class_property
    def _base_entity_class(cls):
        """
        gets base entity class of application.

        it should return type of `BaseEntity` class itself.
        this method is required to overcome circular dependency problem as mixin
        module could not import `BaseEntity` because `BaseEntity` itself references
        to mixin module. and also we could not inject `BaseEntity` dependency through
        `__init__()` method of `MagicMethodMixin` class, because sqlalchemy does not
        call `__init__()` method of entities for populating database results, so
        `__init__()` call is not guaranteed and will only take place on user code.
        so we have to define this method to get `BaseEntity` type here.
        and this is more beautiful than importing `BaseEntity` inside a method
        of `MagicMethodMixin` class.

        :rtype: type[BaseEntity]
        """

        return BaseEntity
