# -*- coding: utf-8 -*-
"""
database paging services module.
"""

from pyrin.application.services import get_component
from pyrin.database.paging import DatabasePagingPackage


def get_default_limit():
    """
    gets default limit in database config store.

    :rtype: int
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).get_default_limit()


def get_default_offset():
    """
    gets default offset in database config store.

    :rtype: int
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).get_default_offset()


def inject_limit(options):
    """
    injects default limit parameter into given dict.

    :param dict options: options dict to inject limit into it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).inject_limit(options)


def inject_offset(options):
    """
    injects default offset parameter into given dict.

    :param dict options: options dict to inject offset into it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).inject_offset(options)


def inject_custom_limit(limit, options):
    """
    injects given limit parameter into given dict.

    :param int limit: limit value to be set in given dict.
    :param dict options: options dict to inject limit into it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).inject_custom_limit(limit, options)


def inject_custom_offset(offset, options):
    """
    injects given offset parameter into given dict.

    :param int offset: offset value to be set in given dict.
    :param dict options: options dict to inject offset into it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).inject_custom_offset(offset, options)


def inject_paging(options):
    """
    injects default limit and offset parameters into given dict.

    :param dict options: options dict to inject limit and offset into it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).inject_paging(options)


def inject_custom_paging(limit, offset, options):
    """
    injects custom limit and offset parameters into given dict.

    :param int limit: limit value to be set in given dict.
    :param int offset: offset value to be set in given dict.
    :param dict options: options dict to inject limit and offset into it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).inject_custom_paging(limit,
                                                                             offset,
                                                                             options)


def extract_limit(options):
    """
    extracts and gets limit parameter from given dict.
    if `__limit__` key is not available in provided
    dict, it gets the value from database config store
    from `paging` section.

    :param dict options: options dict to get limit from it.

    :rtype: int
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).extract_limit(options)


def extract_offset(options):
    """
    extracts and gets offset parameter from given dict.
    if `__offset__` key is not available in provided
    dict, it gets the value from database config store
    from `paging` section.

    :param dict options: options dict to get offset from it.

    :rtype: int
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).extract_offset(options)


def extract_paging(options):
    """
    extracts and gets limit and offset parameters from given dict.
    if `__limit__` or `__offset__` key is not available in provided
    dict, it gets the value from database config store
    from `paging` section.

    :param dict options: options dict to get limit and offset from it.

    :returns: tuple(int limit, int offset)
    :rtype: tuple
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).extract_paging(options)


def is_paging_required(options):
    """
    gets a value indicating that paging should be done.
    it checks a key with name `__paging__` is available in dict
    and its value is set to True, otherwise returns False.

    :param dict options: options dict to detect paging should be done from it.

    :rtype: bool
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).is_paging_required(options)
