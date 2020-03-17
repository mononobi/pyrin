# -*- coding: utf-8 -*-
"""
model base module.
"""

from sqlalchemy.ext.declarative import as_declarative

from pyrin.database.model.mixin import CRUDMixin, MagicMethodMixin, QueryMixin


class BaseEntity(MagicMethodMixin, CRUDMixin, QueryMixin):
    """
    base entity class.

    it should be used as the base class by for every declarative base class.
    for example `CoreEntity`, which by default is the application's declarative
    base class, inherits from this.

    if you want to implement a new declarative base class for your application models
    instead of `CoreEntity`, you must inherit your new base class from `BaseEntity`.
    because application will check isinstance() on this class's type to detect models.
    the new base class must have `@as_declarative` decorator on it.
    note that your application must have a unique declarative base class for all
    models, do not mix the use of your new base class and `CoreEntity`, otherwise
    you will face problems in migrations and also multi-database environments.
    """

    # holds the table name in database.
    __tablename__ = None

    # holds the extra arguments for table.
    # for example:
    # __table_args__ = {'schema': 'database_name.schema_name',
    #                   'extend_existing': True}
    __table_args__ = None

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of BaseEntity.

        note that this method will only be called on user code, meaning
        that results returned by orm from database will not call `__init__`
        of each entity.

        it also could set attributes on the constructed instance using the
        names and values in `kwargs`. all keys that are present as either mapped
        columns or relationship properties of the instance's class are allowed.

        :raises ColumnNotExistedError: column not existed error.
        """

        super().__init__()

        self._set_name(self.__class__.__name__)
        self.from_dict(False, **kwargs)

    @property
    def _base_entity_class(self):
        """
        gets base entity class of application.

        it should return type of `BaseEntity` class itself.
        this method is required to overcome circular dependency problem as mixin
        module could not import `BaseEntity` because `BaseEntity` itself references
        to mixin module. and also we could not inject `BaseEntity` dependency through
        `__init_()` method of `MagicMethodMixin` class, because sqlalchemy does not
        call `__init__()` method of entities for populating database results, so
        `__init__()` call is not guaranteed and will only take place on user code.
        so we have to define this method to get `BaseEntity` type here.
        and this is more beautiful then importing `BaseEntity` inside a method
        of `MagicMethodMixin` class.

        :rtype: type[BaseEntity]
        """

        return BaseEntity

    @classmethod
    def table_name(cls):
        """
        gets the table name that this entity represents in database.

        :rtype: str
        """

        return cls.__tablename__

    @classmethod
    def table_schema(cls):
        """
        gets the table schema that this entity represents in database.

        it might be `None` if schema has not been set for this entity.

        :rtype: str
        """

        schema = None
        if cls.__table_args__ is not None:
            schema = cls.__table_args__.get('schema', None)

        return schema

    @classmethod
    def table_fullname(cls):
        """
        gets the table fullname that this entity represents in database.

        fullname is `schema.table_name` if schema is available, otherwise it
        defaults to `table_name`.

        :rtype: str
        """

        schema = cls.table_schema()
        name = cls.table_name()

        if schema is not None:
            return '{schema}.{name}'.format(schema=schema, name=name)
        else:
            return name


@as_declarative(constructor=None)
class CoreEntity(BaseEntity):
    """
    core entity class.

    it should be used as the base class for all application concrete models.

    it is also possible to implement a new customized declarative base class for your
    application models. to do this you must subclass it from `BaseEntity`, because
    application will check isinstance() on `BaseEntity` type to detect models. then
    implement customized or new features in your subclassed `BaseEntity`. keep in mind
    that you should not subclass directly from `CoreEntity`, because it has `@as_declarative`
    decorator and sqlalchemy raises an error if you subclass from this as your new declarative
    base class. note that your application must have a unique declarative base class for all
    models, do not mix the use of your new base class and `CoreEntity`, otherwise you will
    face problems in migrations and also multi-database environments.
    """
    pass
