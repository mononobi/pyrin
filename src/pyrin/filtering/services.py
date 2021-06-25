# -*- coding: utf-8 -*-
"""
filtering services module.
"""

from pyrin.application.services import get_component
from pyrin.filtering import FilteringPackage


def filter(entity, *ignore, **filters):
    """
    gets filtering expressions for given entity type based on given filters.

    :param type[pyrin.database.model.base.BaseEntity] entity: entity class type to
                                                              be used for filtering.

    :param sqlalchemy.orm.attributes.InstrumentedAttribute ignore: columns to be ignored
                                                                   from filtering.

    :returns: list of expressions for filtering.
    :rtype: list
    """

    return get_component(FilteringPackage.COMPONENT_NAME).filter(entity, *ignore, **filters)
