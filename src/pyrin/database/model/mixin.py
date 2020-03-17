# -*- coding: utf-8 -*-
"""
model mixin module.

this module provides mixin classes for different features of declarative base entity.
if you want to implement a new declarative base class and not use the `CoreEntity`
provided by pyrin, you could define your new base class and it must be inherited
from `BaseEntity`, because application will check isinstance() on `BaseEntity` type
to detect models. and then implement your customized or new features in your base class.
then you must put `@as_declarative` decorator on your new base class. now all your concrete
entities must be inherited from the new declarative base class. note that you must use a
unique declarative base class for all your models, do not mix `CoreEntity` and your new
declarative base class usage. otherwise you will face problems in migrations and also
multi-database environments.
"""

import inspect

from abc import abstractmethod

from sqlalchemy import inspect as sqla_inspect
from sqlalchemy.exc import NoInspectionAvailable

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.services import get_current_store
from pyrin.core.context import CoreObject, DTO
from pyrin.database.model.exceptions import ColumnNotExistedError, \
    InvalidDeclarativeBaseTypeError


class ColumnMixin(CoreObject):
    """
    column mixin class.

    this class adds functionalities about columns to its subclasses.
    """

    def _set_all_columns(self, columns):
        """
        sets all column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_all_columns', None) is None:
            self.__class__._all_columns = DTO()

        self.__class__._all_columns[type(self)] = columns

    def _set_exposed_columns(self, columns):
        """
        sets exposed column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_exposed_columns', None) is None:
            self.__class__._exposed_columns = DTO()

        self.__class__._exposed_columns[type(self)] = columns

    @property
    def all_columns(self):
        """
        gets all column names of this entity.

        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        columns = self._get_all_columns()
        if columns is None:
            info = sqla_inspect(type(self))
            columns = tuple(attr.key for attr in info.column_attrs)
            self._set_all_columns(columns)

        return columns

    @property
    def exposed_columns(self):
        """
        gets exposed column names of this entity, which are those that have `exposed=True`.

        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        columns = self._get_exposed_columns()
        if columns is None:
            info = sqla_inspect(type(self))
            columns = tuple(attr.key for attr in info.column_attrs
                            if attr.columns[0].exposed is True)
            self._set_exposed_columns(columns)

        return columns

    def _get_all_columns(self):
        """
        gets all column names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        columns = getattr(self, '_all_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def _get_exposed_columns(self):
        """
        gets exposed column names of this entity, which are those that have `exposed=True`.

        returns None if not found.

        :rtype: tuple[str]
        """

        columns = getattr(self, '_exposed_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None


class RelationshipMixin(CoreObject):
    """
    relationship mixin class.

    this class adds functionalities about relationship properties to its subclasses.
    """

    def _set_relationships(self, relationships):
        """
        sets relationship property names attribute for this class.

        :param tuple[str] relationships: relationship property names.
        """

        if getattr(self, '_relationships', None) is None:
            self.__class__._relationships = DTO()

        self.__class__._relationships[type(self)] = relationships

    @property
    def relationships(self):
        """
        gets all relationship property names of this entity.

        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        relationships = self._get_relationships()
        if relationships is None:
            info = sqla_inspect(type(self))
            relationships = tuple(attr.key for attr in info.relationships)
            self._set_relationships(relationships)

        return relationships

    def _get_relationships(self):
        """
        gets all relationship property names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        relationships = getattr(self, '_relationships', None)
        if relationships is not None:
            return relationships.get(type(self), None)

        return None


class PropertyMixin(ColumnMixin, RelationshipMixin):
    """
    property mixin class.

    this class adds functionalities about column and
    relationship properties to its subclasses.
    """

    def _set_all_columns_and_relationships(self, all_properties):
        """
        sets all column and relationship property names attribute for this class.

        :param tuple[str] all_properties: all property names.
        """

        if getattr(self, '_all_columns_and_relationships', None) is None:
            self.__class__._all_columns_and_relationships = DTO()

        self.__class__._all_columns_and_relationships[type(self)] = all_properties

    def _set_exposed_columns_and_relationships(self, exposed_properties):
        """
        sets exposed column and relationship property names attribute for this class.

        exposed columns are those that have `exposed=True` in their definition.

        :param tuple[str] exposed_properties: exposed property names.
        """

        if getattr(self, '_exposed_columns_and_relationships', None) is None:
            self.__class__._exposed_columns_and_relationships = DTO()

        self.__class__._exposed_columns_and_relationships[type(self)] = exposed_properties

    @property
    def all_columns_and_relationships(self):
        """
        gets all column and relationship property names of this entity.

        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        all_properties = self._get_all_columns_and_relationships()
        if all_properties is None:
            all_properties = self.all_columns + self.relationships
            self._set_all_columns_and_relationships(all_properties)

        return all_properties

    @property
    def exposed_columns_and_relationships(self):
        """
        gets exposed column and relationship property names of this entity.

        exposed columns are those that have `exposed=True` is their definition.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        exposed_properties = self._get_exposed_columns_and_relationships()
        if exposed_properties is None:
            exposed_properties = self.exposed_columns + self.relationships
            self._set_exposed_columns_and_relationships(exposed_properties)

        return exposed_properties

    def _get_all_columns_and_relationships(self):
        """
        gets all column and relationship property names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        all_properties = getattr(self, '_all_columns_and_relationships', None)
        if all_properties is not None:
            return all_properties.get(type(self), None)

        return None

    def _get_exposed_columns_and_relationships(self):
        """
        gets exposed column and relationship property names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        exposed_properties = getattr(self, '_exposed_columns_and_relationships', None)
        if exposed_properties is not None:
            return exposed_properties.get(type(self), None)

        return None


class PrimaryKeyMixin(CoreObject):
    """
    primary key mixin class.

    this class adds functionalities about primary key columns to its subclasses.
    """

    def _is_primary_key_comparable(self, primary_key):
        """
        gets a value indicating that given primary key is comparable.

        the primary key is comparable if it is not None for single
        primary keys and if all the values in primary key tuple are
        not None for composite primary keys.

        :param object | tuple[object] primary_key: primary key value.

        :rtype: bool
        """

        if primary_key is None:
            return False

        if isinstance(primary_key, tuple):
            if len(primary_key) <= 0:
                return False
            else:
                return all(pk is not None for pk in primary_key)

        return True

    def primary_key(self, as_tuple=False):
        """
        gets the primary key value for this entity.

        it could be a single value or a tuple of values
        for composite primary keys.
        it could return None if no primary key is set for this entity.

        :param bool as_tuple: specifies that primary key value must be returned
                              as a tuple even if it's a single value.
                              defaults to False if not provided.

        :rtype: object | tuple[object]
        """

        columns = self.primary_key_columns
        if len(columns) <= 0:
            return None

        if as_tuple is False and len(columns) == 1:
            return getattr(self, columns[0])
        else:
            return tuple(getattr(self, col) for col in columns)

    def _set_primary_key_columns(self, columns):
        """
        sets primary key column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_primary_key_columns', None) is None:
            self.__class__._primary_key_columns = DTO()

        self.__class__._primary_key_columns[type(self)] = columns

    def _get_primary_keys(self):
        """
        gets current entity's primary key column names if available.

        :rtype: tuple[str]
        """

        columns = getattr(self, '_primary_key_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    @property
    def primary_key_columns(self):
        """
        gets the primary key column names of this entity.

        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        pk = self._get_primary_keys()
        if pk is None:
            info = sqla_inspect(type(self))
            pk = tuple(info.get_property_by_column(col).key for col in info.primary_key)
            self._set_primary_key_columns(pk)

        return pk


class ConverterMixin(PropertyMixin):
    """
    converter mixin class.

    this class adds functionalities to convert dict to
    entity and vice versa to its subclasses.
    """

    def to_dict(self, exposed_only=True, **options):
        """
        converts the entity into a dict and returns it.

        the result dict only contains the exposed columns of
        the entity which are those that their `exposed` attribute
        is set to True.

        :param bool exposed_only: if set to False, it returns all
                                  columns of the entity as dict.
                                  if not provided, defaults to True.

        :keyword list[str] columns: the column names to be included in result.
                                    if not provided, the columns in exposed
                                    columns or all columns will be returned.
                                    note that the columns must be a subset of
                                    all columns or exposed columns of this
                                    entity considering "exposed_only" parameter,
                                    otherwise it raises an error.

        :raises ColumnNotExistedError: column not existed error.

        :rtype: dict
        """

        base_columns = None
        requested_columns = options.get('columns', None)

        if exposed_only is False:
            base_columns = self.all_columns
        else:
            base_columns = self.exposed_columns

        result = DTO()
        if requested_columns is None or len(requested_columns) <= 0:
            requested_columns = base_columns

        difference = set(requested_columns).difference(set(base_columns))
        if len(difference) > 0:
            raise ColumnNotExistedError('Requested columns {columns} are '
                                        'not available in entity [{entity}].'
                                        'it might be because of "exposed_only" '
                                        'parameter value passed to this method.'
                                        .format(columns=list(difference), entity=self))
        for col in requested_columns:
            result[col] = getattr(self, col)

        return result

    def from_dict(self, silent_on_invalid_column=True, **kwargs):
        """
        updates the column values of this entity with values in keyword arguments.

        it could fill columns and also relationship properties if provided.

        :param bool silent_on_invalid_column: specifies that if a key is not available
                                              in entity columns, do not raise an error.
                                              defaults to True if not provided.

        :raises ColumnNotExistedError: column not existed error.
        """

        all_properties = self.all_columns_and_relationships
        for key, value in kwargs.items():
            if key in all_properties:
                setattr(self, key, value)
            else:
                if silent_on_invalid_column is False:
                    raise ColumnNotExistedError('Entity [{entity}] does not have '
                                                'a column or relationship attribute '
                                                'named [{column}].'
                                                .format(entity=self,
                                                        column=key))


class MagicMethodMixin(PrimaryKeyMixin):
    """
    magic method mixin class.

    this class adds different magic method implementations to its subclasses.
    """

    def __eq__(self, other):
        if isinstance(other, self.root_base_class):
            if self._is_primary_key_comparable(self.primary_key()) is True:
                return self.primary_key() == other.primary_key()
            else:
                return self is other

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self._is_primary_key_comparable(self.primary_key()) is True:
            return hash('{root_base}.{pk}'.format(root_base=self.root_base_class,
                                                  pk=self.primary_key()))

        return super().__hash__()

    def __repr__(self):
        """
        gets the string representation of current entity.

        :rtype: str
        """
        return '{module}.{name} [{pk}]'.format(module=self.__module__,
                                               name=self.get_name(),
                                               pk=self.primary_key())

    def _set_root_base_class(self, root_base_class):
        """
        sets root base class of this entity.

        root base class is the class which is direct subclass
        of declarative base class (which by default is CoreEntity)
        in inheritance hierarchy.

        for example if you use pyrin's default CoreEntity as your base model:
        {CoreEntity -> BaseEntity, A -> CoreEntity, B -> A, C -> B}
        then, root base class of A, B and C is A.

        if you implement a new base class named MyNewDeclarativeBase as base model:
        {MyNewDeclarativeBase -> BaseEntity, A -> MyNewDeclarativeBase, B -> A, C -> B}
        then, root base class of A, B and C is A.

        the inheritance rule also supports multi-branch hierarchy. for example:
        {CoreEntity -> BaseEntity, A -> CoreEntity, B -> A, C -> A}
        then, root base class of A, B and C is A.

        :param type root_base_class: root base class type.
        """

        self.__class__._root_base_class = root_base_class

    def _get_root_base_class(self):
        """
        gets root base class of this entity and caches it.

        returns None if it's not set.

        root base class is the class which is direct subclass
        of declarative base class (which by default is CoreEntity)
        in inheritance hierarchy.

        for example if you use pyrin's default CoreEntity as your base model:
        {CoreEntity -> BaseEntity, A -> CoreEntity, B -> A, C -> B}
        then, root base class of A, B and C is A.

        if you implement a new base class named MyNewDeclarativeBase as base model:
        {MyNewDeclarativeBase -> BaseEntity, A -> MyNewDeclarativeBase, B -> A, C -> B}
        then, root base class of A, B and C is A.

        the inheritance rule also supports multi-branch hierarchy. for example:
        {CoreEntity -> BaseEntity, A -> CoreEntity, B -> A, C -> A}
        then, root base class of A, B and C is A.

        :rtype: type
        """

        return getattr(self, '_root_base_class', None)

    @property
    def root_base_class(self):
        """
        gets root base class of this entity.

        root base class will be calculated once and cached.

        :rtype: type
        """

        base = self._get_root_base_class()
        if base is None:
            bases = inspect.getmro(type(self))
            root_base_entity_index = bases.index(self.declarative_base_class) - 1
            base = bases[root_base_entity_index]
            self._set_root_base_class(base)

        return base

    @property
    def declarative_base_class(self):
        """
        gets declarative base class of application.

        :rtype: type
        """

        base = self._get_declarative_base_class()
        if base is None:
            bases = inspect.getmro(type(self))
            base_entity_index = bases.index(self._base_entity_class)
            potential_declarative_bases = bases[0:base_entity_index]
            base = self._extract_declarative_base(potential_declarative_bases)
            self._set_declarative_base_class(base)

        return base

    def _extract_declarative_base(self, types):
        """
        extracts the first declarative base found from given types.

        returns None if not found.

        :param tuple[type] types: class types to extract declarative base from them.

        :rtype: type
        """

        for item in types:
            try:
                sqla_inspect(item)
            except NoInspectionAvailable:
                return item

        return None

    def _set_declarative_base_class(self, declarative_base_class):
        """
        sets declarative base class of application.

        the value will be set and shared for all entities because there
        should be only one declarative base class.

        :param type declarative_base_class: a class type of application declarative base class.
                                            by default, it would be `CoreEntity` class.
        """

        self._validate_declarative_base_class(declarative_base_class)
        MagicMethodMixin._declarative_base_class = declarative_base_class

    def _get_declarative_base_class(self):
        """
        gets declarative base class of application.

        returns None if it's not set.

        :rtype: type
        """

        return getattr(self, '_declarative_base_class', None)

    @property
    @abstractmethod
    def _base_entity_class(self):
        """
        gets base entity class of application.

        this method must be overridden by `BaseEntity` class.
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

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()

    def _validate_declarative_base_class(self, declarative_base_class):
        """
        validates the given declarative base class.

        :param type declarative_base_class: a class type of application declarative base class.
                                            by default, it would be `CoreEntity` class.

        :raises InvalidDeclarativeBaseTypeError: invalid declarative base type error.
        """

        if declarative_base_class is None or not inspect.isclass(declarative_base_class):
            raise InvalidDeclarativeBaseTypeError('Input parameter [{declarative}] '
                                                  'is not a class.'
                                                  .format(declarative=declarative_base_class))

        if not issubclass(declarative_base_class, self._base_entity_class):
            raise InvalidDeclarativeBaseTypeError('Input parameter [{declarative}] '
                                                  'in not a subclass of [{base}].'
                                                  .format(declarative=declarative_base_class,
                                                          base=self._base_entity_class))


class QueryMixin(CoreObject):
    """
    query mixin class.

    this class adds query method to its subclasses.
    the query method will always use the correct session
    based on request context availability.
    """

    @classmethod
    def query(cls, *entities, **options):
        """
        gets the query object to perform queries on it.

        it always uses the correct session based on request context availability.

        :param BaseEntity entities: entities or columns to use them in query.
                                    if not provided, it uses all columns of this entity.

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

        :rtype: CoreQuery
        """

        store = get_current_store()
        used_entities = entities
        if entities is None or len(entities) <= 0:
            used_entities = (cls,)

        return store.query(*used_entities, **options)


class CRUDMixin(ConverterMixin):
    """
    crud mixin class.

    this class adds CRUD functionalities to is subclasses.
    it includes save, update and delete.
    it uses the correct session based on request context availability.
    """

    def save(self):
        """
        saves the current entity.
        """

        store = get_current_store()
        store.add(self)
        return self

    def update(self, silent_on_invalid_column=True, **kwargs):
        """
        updates the column values of this entity with values in keyword arguments.

        it could fill columns and also relationship properties if provided.

        :param bool silent_on_invalid_column: specifies that if a key is not available
                                              in entity columns, do not raise an error.
                                              defaults to True if not provided.

        :raises ColumnNotExistedError: column not existed error.
        """

        self.from_dict(silent_on_invalid_column, **kwargs)
        return self.save()

    def delete(self):
        """
        deletes the current entity.
        """

        store = get_current_store()
        store.delete(self)
