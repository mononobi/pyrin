# -*- coding: utf-8 -*-
"""
database paging services module.
"""

from pyrin.application.services import get_component
from pyrin.database.paging import DatabasePagingPackage


def extract_paging_params(values):
    """
    extracts paging parameters from given dict and returns them as a new dict.

    the values will be removed from input dict.

    :param dict values: a dict to extract paging params from it.

    :returns: dict(int page: page number,
                   int page_size: page size)
    :rtype: dict
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).extract_paging_params(values)


def get_paging_params(**options):
    """
    gets paging parameters from given inputs.

    note that this method does not do any validation and just returns
    keys as they are, even if their value is None.

    :keyword int page: page number.
    :keyword int page_size: page size.

    :returns: tuple[int page, int page_size]
    :rtype: tuple[int, int]
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).get_paging_params(**options)


def generate_paging_params(page, page_size):
    """
    generates paging parameters from given inputs.

    :param int page: page number.
    :param int page_size: page size.

    :returns: dict[int page, int page_size]
    :rtype: dict[int, int]
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).generate_paging_params(page,
                                                                                      page_size)


def inject_paging_keys(limit, offset, values):
    """
    injects paging keys into given dict.

    :param int limit: limit.
    :param int offset: offset.
    :param dict values: a dict to inject paging keys into it.
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).inject_paging_keys(
        limit, offset, values)


def get_paging_keys(**options):
    """
    gets paging keys from given inputs.

    note that this method does not do any validation and just returns
    keys as they are, even if their value is None.

    :keyword int __limit__: limit value.
    :keyword int __offset__: offset value.

    :returns: tuple[int limit, int offset]
    :rtype: tuple[int, int]
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).get_paging_keys(**options)


def disable_paging_keys(values):
    """
    disables paging keys in given dict.

    :param dict values: a dict to disable paging keys in it.
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).disable_paging_keys(values)
