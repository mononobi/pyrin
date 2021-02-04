# -*- coding: utf-8 -*-
"""
database bulk services module.
"""

from pyrin.application.services import get_component
from pyrin.database.bulk import DatabaseBulkPackage


def insert(*entities, **options):
    """
    bulk inserts the given entities.

    note that entities must be from the same type.

    :param BaseEntity entities: entities to be inserted.

    :keyword int chunk_size: chunk size to insert values.
                             after each chunk, store will be flushed.
                             if not provided, all values will be inserted
                             in a single call and no flush will occur.

    :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                  which has `allow_read=False` or its name
                                                  starts with underscore `_`, should not
                                                  be included in result dict. defaults to
                                                  `SECURE_TRUE` if not provided.

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
                                                       available in result, they will
                                                       be ignored.

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
    """

    return get_component(DatabaseBulkPackage.COMPONENT_NAME).insert(*entities, **options)


def update(*entities, **options):
    """
    bulk updates the given entities.

    note that entities must be from the same type.

    :param BaseEntity entities: entities to be updated.

    :keyword int chunk_size: chunk size to update values.
                             after each chunk, store will be flushed.
                             if not provided, all values will be updated
                             in a single call and no flush will occur.

    :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                  which has `allow_read=False` or its name
                                                  starts with underscore `_`, should not
                                                  be included in result dict. defaults to
                                                  `SECURE_TRUE` if not provided.

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
                                                       available in result, they will
                                                       be ignored.

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
    """

    return get_component(DatabaseBulkPackage.COMPONENT_NAME).update(*entities, **options)
