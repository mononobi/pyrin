# -*- coding: utf-8 -*-
"""
filtering services module.
"""

from pyrin.application.services import get_component
from pyrin.filtering import FilteringPackage


def filter(entity, filters, *ignore, **options):
    """
    gets filtering expressions for given entity type based on given filters.

    :param type[pyrin.database.model.base.BaseEntity] entity: entity class type to
                                                              be used for filtering.

    :param dict filters: filters to be applied.

    :param sqlalchemy.orm.attributes.InstrumentedAttribute ignore: columns to be ignored
                                                                   from filtering.

    :keyword bool remove: remove all keys that are applied as filter from filters input.
                          defaults to True if not provided.

    :keyword bool readable: specifies that any column or attribute
                            which has `allow_read=False` or its name
                            starts with underscore `_`, should not
                            be included in filtering.
                            defaults to True if not provided.

    :returns: list of expressions for filtering.
    :rtype: list
    """

    return get_component(FilteringPackage.COMPONENT_NAME).filter(entity, filters,
                                                                 *ignore, **options)
