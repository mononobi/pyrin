# -*- coding: utf-8 -*-
"""
filtering services module.
"""

from pyrin.application.services import get_component
from pyrin.filtering import FilteringPackage


def filter(entity, filters, *ignore):
    """
    gets filtering expressions for given entity type based on given filters.

    it removes all keys that are applied as filter from filters input.

    :param type[pyrin.database.model.base.BaseEntity] entity: entity class type to
                                                              be used for filtering.

    :param dict filters: filters to be applied.

    :param sqlalchemy.orm.attributes.InstrumentedAttribute ignore: columns to be ignored
                                                                   from filtering.

    :returns: list of expressions for filtering.
    :rtype: list
    """

    return get_component(FilteringPackage.COMPONENT_NAME).filter(entity, filters, *ignore)
