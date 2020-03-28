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

import pyrin.database.model.services as model_services
import pyrin.configuration.services as config_services

from pyrin.core.globals import LIST_TYPES
from pyrin.utils.custom_print import print_warning
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.services import get_current_store
from pyrin.core.structs import CoreObject, DTO
from pyrin.database.model.exceptions import ColumnNotExistedError, \
    InvalidDeclarativeBaseTypeError, InvalidDepthProvidedError


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

        if getattr(ColumnMixin, '_all_columns', None) is None:
            ColumnMixin._all_columns = DTO()

        ColumnMixin._all_columns[type(self)] = columns

    def _set_exposed_columns(self, columns):
        """
        sets exposed column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(ColumnMixin, '_exposed_columns', None) is None:
            ColumnMixin._exposed_columns = DTO()

        ColumnMixin._exposed_columns[type(self)] = columns

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

        columns = getattr(ColumnMixin, '_all_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def _get_exposed_columns(self):
        """
        gets exposed column names of this entity, which are those that have `exposed=True`.

        returns None if not found.

        :rtype: tuple[str]
        """

        columns = getattr(ColumnMixin, '_exposed_columns', None)
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

        if getattr(RelationshipMixin, '_relationships', None) is None:
            RelationshipMixin._relationships = DTO()

        RelationshipMixin._relationships[type(self)] = relationships

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

        relationships = getattr(RelationshipMixin, '_relationships', None)
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

        if getattr(PropertyMixin, '_all_columns_and_relationships', None) is None:
            PropertyMixin._all_columns_and_relationships = DTO()

        PropertyMixin._all_columns_and_relationships[type(self)] = all_properties

    def _set_exposed_columns_and_relationships(self, exposed_properties):
        """
        sets exposed column and relationship property names attribute for this class.

        exposed columns are those that have `exposed=True` in their definition.

        :param tuple[str] exposed_properties: exposed property names.
        """

        if getattr(PropertyMixin, '_exposed_columns_and_relationships', None) is None:
            PropertyMixin._exposed_columns_and_relationships = DTO()

        PropertyMixin._exposed_columns_and_relationships[type(self)] = exposed_properties

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

        all_properties = getattr(PropertyMixin, '_all_columns_and_relationships', None)
        if all_properties is not None:
            return all_properties.get(type(self), None)

        return None

    def _get_exposed_columns_and_relationships(self):
        """
        gets exposed column and relationship property names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        exposed_properties = getattr(PropertyMixin, '_exposed_columns_and_relationships', None)
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

        if getattr(PrimaryKeyMixin, '_primary_key_columns', None) is None:
            PrimaryKeyMixin._primary_key_columns = DTO()

        PrimaryKeyMixin._primary_key_columns[type(self)] = columns

    def _get_primary_keys(self):
        """
        gets current entity's primary key column names if available.

        :rtype: tuple[str]
        """

        columns = getattr(PrimaryKeyMixin, '_primary_key_columns', None)
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

    # maximum valid depth for conversion.
    # note that higher depth values may cause performance issues or
    # application failure in some cases. so if you do not know how
    # much depth is required for conversion, start without providing depth.
    MAX_DEPTH = 5

    def to_dict(self, **options):
        """
        converts the entity into a dict and returns it.

        it could convert columns and also relationship properties
        if `depth` is provided.
        the result dict by default only contains the exposed columns of the
        entity which are those that their `exposed` attribute is set to True.

        :keyword bool exposed_only: if set to False, it returns all
                                    columns of the entity as dict.
                                    if not provided, defaults to True.

        :keyword dict[str, list[str]] | list[str] columns: column names to be included in result.
                                                           it could be a list of column names.
                                                           for example:
                                                           `columns=['id', 'name', 'age']`
                                                           but if you want to include
                                                           relationships, then columns for each
                                                           entity must be provided in a key for
                                                           that entity class name.
                                                           for example if there is `CarEntity` and
                                                           `PersonEntity`, it should be like this:
                                                           `columns=dict(CarEntity=
                                                                         ['id', 'name'],
                                                                         PersonEntity=
                                                                         ['id', 'age'])`
                                                           if provided column names are not
                                                           available in result, an error will
                                                           be raised.

        :note columns: dict[str entity_class_name, list[str column_name]] | list[str column_name]

        :keyword dict[str, dict[str, str]] | dict[str, str] rename: column names that must be
                                                                    renamed in the result.
                                                                    it could be a dict with keys
                                                                    as original column names and
                                                                    values as new column names
                                                                    that should be exposed instead
                                                                    of original column names.
                                                                    for example:
                                                                    `rename=dict(age='new_age',
                                                                                 name='new_name')`
                                                                    but if you want to include
                                                                    relationships, then you must
                                                                    provide a dict containing
                                                                    entity class name as key and
                                                                    for value, another dict
                                                                    containing original column
                                                                    names as keys, and column
                                                                    names that must be exposed
                                                                    instead of original names,
                                                                    as values. for example
                                                                    if there is `CarEntity` and `
                                                                    PersonEntity`, it should be
                                                                    like this:
                                                                    `rename=
                                                                    dict(CarEntity=
                                                                         dict(name='new_name'),
                                                                         PersonEntity=
                                                                         dict(age='new_age')`
                                                                    then, the value of `name`
                                                                    column in result will be
                                                                    returned as `new_name` column.
                                                                    and also value of `age` column
                                                                    in result will be returned as
                                                                    'new_age' column. if provided
                                                                    rename columns are not
                                                                    available in result, they
                                                                    will be ignored.

        :note rename: dict[str entity_class_name, dict[str original_column, str new_column]] |
                      dict[str original_column, str new_column]

        :keyword dict[str, list[str]] | list[str] exclude: column names to be excluded from
                                                           result. it could be a list of column
                                                           names. for example:
                                                           `exclude=['id', 'name', 'age']`
                                                           but if you want to include
                                                           relationships, then columns for each
                                                           entity must be provided in a key for
                                                           that entity class name.
                                                           for example if there is `CarEntity`
                                                           and `PersonEntity`, it should be
                                                           like this:
                                                           `exclude=dict(CarEntity=
                                                                         ['id', 'name'],
                                                                         PersonEntity=
                                                                         ['id', 'age'])`
                                                            if provided excluded columns are not
                                                            available in result, they will be
                                                            ignored.

        :note exclude: dict[str entity_class_name, list[str column_name]] | list[str column_name]

        :keyword int depth: a value indicating the depth for conversion.
                            for example if entity A has a relationship with
                            entity B and there is a list of B in A, if `depth=0`
                            is provided, then just columns of A will be available
                            in result dict, but if `depth=1` is provided, then all
                            B entities in A will also be included in the result dict.
                            actually, `depth` specifies that relationships in an
                            entity should be followed by how much depth.
                            note that, if `columns` is also provided, it is required to
                            specify relationship property names in provided columns.
                            otherwise they won't be included even if `depth` is provided.
                            defaults to `default_depth` value of database config store.
                            please be careful on increasing `depth`, it could fail
                            application if set to higher values. choose it wisely.
                            normally the maximum acceptable `depth` would be 2 or 3.
                            there is a hard limit for max valid `depth` which is set
                            in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                            `depth` value than this limit, will cause an error.

        :raises ColumnNotExistedError: column not existed error.
        :raises InvalidDepthProvidedError: invalid depth provided error.

        :rtype: dict
        """

        base_columns_and_relationships = None
        requested_columns, rename, excluded_columns = self._extract_conditions(**options)

        exposed_only = options.get('exposed_only', True)
        if exposed_only is None:
            exposed_only = True

        depth = options.get('depth', None)
        if depth is None:
            depth = config_services.get('database', 'conversion', 'default_depth')

        if exposed_only is False:
            base_columns_and_relationships = self.all_columns_and_relationships
        else:
            base_columns_and_relationships = self.exposed_columns_and_relationships

        relations = self.relationships
        requested_relationships = []

        if len(requested_columns) > 0:
            difference = set(requested_columns).difference(set(base_columns_and_relationships))
            if len(difference) > 0:
                raise ColumnNotExistedError('Requested columns or relationship properties '
                                            '{columns} are not available in entity [{entity}]. '
                                            'it might be because of "exposed_only" '
                                            'parameter value passed to this method.'
                                            .format(columns=list(difference), entity=self))
        else:
            requested_columns = base_columns_and_relationships

        result = DTO()
        for col in requested_columns:
            if col not in excluded_columns:
                if col in relations:
                    requested_relationships.append(col)
                else:
                    result[rename.get(col, col)] = getattr(self, col)

        if depth > 0 and len(requested_relationships) > 0:
            if depth > self.MAX_DEPTH:
                raise InvalidDepthProvidedError('Maximum valid "depth" for conversion '
                                                'is [{max_depth}]. provided depth '
                                                '[{invalid_depth}] is invalid.'
                                                .format(max_depth=self.MAX_DEPTH,
                                                        invalid_depth=depth))

            options.update(depth=depth - 1)
            for relation in requested_relationships:
                value = getattr(self, relation)
                new_name = rename.get(relation, relation)
                result[new_name] = None
                if value is not None:
                    if isinstance(value, LIST_TYPES):
                        result[new_name] = []
                        if len(value) > 0:
                            for entity in value:
                                result[new_name].append(entity.to_dict(**options))
                    else:
                        result[new_name] = value.to_dict(**options)

        return result

    def from_dict(self, silent_on_invalid_column=True, **kwargs):
        """
        updates the column values of this entity with values in keyword arguments.

        it could fill columns and also relationship properties if provided.
        note that relationship values must be entities. this method could not convert
        relationships which are dict, into entities.

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

    def _extract_conditions(self, **options):
        """
        extracts all conditions available in given options.

        it extracts columns, rename and exclude values.

        :keyword dict[str, list[str]] | list[str] columns: column names to be included in result.
                                                           it could be a list of column names.
                                                           for example:
                                                           `columns=['id', 'name', 'age']`
                                                           but if you want to include
                                                           relationships, then columns for each
                                                           entity must be provided in a key for
                                                           that entity class name.
                                                           for example if there is `CarEntity` and
                                                           `PersonEntity`, it should be like this:
                                                           `columns=dict(CarEntity=
                                                                         ['id', 'name'],
                                                                         PersonEntity=
                                                                         ['id', 'age'])`
                                                           if provided column names are not
                                                           available in result, an error will
                                                           be raised.

        :note columns: dict[str entity_class_name, list[str column_name]] | list[str column_name]

        :keyword dict[str, dict[str, str]] | dict[str, str] rename: column names that must be
                                                                    renamed in the result.
                                                                    it could be a dict with keys
                                                                    as original column names and
                                                                    values as new column names
                                                                    that should be exposed instead
                                                                    of original column names.
                                                                    for example:
                                                                    `rename=dict(age='new_age',
                                                                                 name='new_name')`
                                                                    but if you want to include
                                                                    relationships, then you must
                                                                    provide a dict containing
                                                                    entity class name as key and
                                                                    for value, another dict
                                                                    containing original column
                                                                    names as keys, and column
                                                                    names that must be exposed
                                                                    instead of original names,
                                                                    as values. for example
                                                                    if there is `CarEntity` and
                                                                    `PersonEntity`, it should be
                                                                    like this:
                                                                    `rename=
                                                                    dict(CarEntity=
                                                                         dict(name='new_name'),
                                                                         PersonEntity=
                                                                         dict(age='new_age')`
                                                                    then, the value of `name`
                                                                    column in result will be
                                                                    returned as `new_name` column.
                                                                    and also value of `age` column
                                                                    in result will be returned as
                                                                    'new_age' column. if provided
                                                                    rename columns are not
                                                                    available in result, they
                                                                    will be ignored.

        :note rename: dict[str entity_class_name, dict[str original_column, str new_column]] |
                      dict[str original_column, str new_column]

        :keyword dict[str, list[str]] | list[str] exclude: column names to be excluded from
                                                           result. it could be a list of column
                                                           names. for example:
                                                           `exclude=['id', 'name', 'age']`
                                                           but if you want to include
                                                           relationships, then columns for each
                                                           entity must be provided in a key for
                                                           that entity class name.
                                                           for example if there is `CarEntity`
                                                           and `PersonEntity`, it should be
                                                           like this:
                                                           `exclude=dict(CarEntity=
                                                                         ['id', 'name'],
                                                                         PersonEntity=
                                                                         ['id', 'age'])`
                                                            if provided excluded columns are not
                                                            available in result, they will be
                                                            ignored.

        :note exclude: dict[str entity_class_name, list[str column_name]] | list[str column_name]

        :returns: tuple[list[str column_name],
                        dict[str original_column, str new_column],
                        list[str excluded_column]]

        :rtype: tuple[list[str], dict[str, str], list[str]]
        """

        columns = options.get('columns', None)
        rename = options.get('rename', None)
        exclude = options.get('exclude', None)

        if isinstance(columns, dict):
            columns = columns.get(self.get_class_name(), None)

        if isinstance(rename, dict) and len(rename) > 0 and \
                isinstance(list(rename.values())[0], dict):

            rename = rename.get(self.get_class_name(), None)

        if isinstance(exclude, dict):
            exclude = exclude.get(self.get_class_name(), None)

        if columns is None:
            columns = []

        if rename is None:
            rename = {}

        if exclude is None:
            exclude = []

        return columns, rename, exclude


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

        setattr(root_base_class, '_root_base_class', root_base_class)

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

        return getattr(MagicMethodMixin, '_declarative_base_class', None)

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

        if declarative_base_class is not model_services.get_declarative_base():
            print_warning('You have implemented a new declarative base type [{new}] '
                          'in your application. to make everything works as expected '
                          'you must override "pyrin.database.model.ModelManager.'
                          'get_declarative_base()" method in your application inside '
                          '"database.model" package. for more information on how to do '
                          'that or how to ignore it, see the documentation of specified '
                          'method.'.format(new=declarative_base_class))


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
