# -*- coding: utf-8 -*-
"""
filtering services module.
"""

from pyrin.application.services import get_component
from pyrin.filtering import FilteringPackage


def filter(filters, *entity, **options):
    """
    gets filtering expressions for given entity types based on given filters.

    **NOTE:**

    if a filter name is available in both `labeled_filters` and columns of
    entities, the value of `labeled_filters` will be used.

    if a filter name is available in columns of more than one entity, the
    first found entity will be used.

    :param dict filters: filters to be applied.

    :param type[pyrin.database.model.base.BaseEntity] entity: entity class type to
                                                              be used for filtering.

    :keyword list[InstrumentedAttribute | hybrid_property] ignore: columns to be ignored
                                                                   from filtering. this
                                                                   only has effect on
                                                                   `entity` and will be
                                                                   ignored for `labeled_filters`.

    :keyword bool remove: remove all keys that are applied as filter from filters input.
                          defaults to True if not provided.

    :keyword bool readable: specifies that any column or attribute
                            which has `allow_read=False` or its name
                            starts with underscore `_`, should not
                            be included in filtering.
                            defaults to True if not provided.
                            this only has effect on `entity` and will be
                            ignored for `labeled_filters`.

    :keyword dict labeled_filters: a dict containing all columns that should have
                                   a different filter name than their actual column
                                   name. for example:
                                   {'city_name': CityEntity.name,
                                    'person_name': PersonEntity.name}

    :keyword bool ignore_duplicates: specifies that if multiple labeled filters
                                     point to the same column and have the same value
                                     in provided filters, only add one of them in
                                     where clause. defaults to True if not provided.
                                     the main usage for this is in admin page which
                                     produces inclusive filters dynamically.

    :returns: list of expressions for filtering.
    :rtype: list
    """

    return get_component(FilteringPackage.COMPONENT_NAME).filter(filters, *entity, **options)


def get_range_filter_names(name):
    """
    gets range filter names for given name.

    it returns a tuple of two items. if name is `created_at`, then
    it returns (`from_created_at`, `to_created_at`) as range filters.

    :param str name: column name.

    :returns: tuple[str lower_bound_name, str upper_bound_name]
    :rtype: tuple[str, str]
    """

    return get_component(FilteringPackage.COMPONENT_NAME).get_range_filter_names(name)


def is_range_supported_type(type_):
    """
    gets a value indicating that range operations are supported for given type.

    :param type type_: type to be checked for range support.

    :rtype: bool
    """

    return get_component(FilteringPackage.COMPONENT_NAME).is_range_supported_type(type_)


def is_range_supported_column(column):
    """
    gets a value indicating that range operations are supported for given column.

    columns which their python type is not in `RANGE_SUPPORTED_TYPES`,
    do not support range operations.

    :param sqlalchemy.orm.attributes.InstrumentedAttribute column: column to be checked
                                                                   for range support.

    :rtype: bool
    """

    return get_component(FilteringPackage.COMPONENT_NAME).is_range_supported_column(column)
