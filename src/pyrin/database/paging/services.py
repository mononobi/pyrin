# -*- coding: utf-8 -*-
"""
database paging services module.
"""

from pyrin.application.services import get_component
from pyrin.database.paging import DatabasePagingPackage


def get_default_limit():
    """
    gets default limit from database config store.

    :rtype: int
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).get_default_limit()


def is_auto_paging():
    """
    gets a value indicating that auto paging is enabled.

    :rtype: bool
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).is_auto_paging()


def enable_limit(options, limit=None):
    """
    enables limit with default or given limit parameter in given dict.

    :param int limit: custom limit value to be injected into given dict.
                      if not provided, defaults to limit value in
                      database config store.

    :param dict options: options dict to inject limit in it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).enable_limit(options, limit)


def disable_limit(options):
    """
    disables limit in given dict. it removes limit key from it.

    :param dict options: options dict to disable limit in it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).disable_limit(options)


def extract_limit(options):
    """
    extracts and gets limit parameter from given dict.
    it returns None if no limit is set in given dict.

    :param dict options: options dict to get limit from it.

    :rtype: int
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).extract_limit(options)


def extract_offset(options):
    """
    extracts and gets offset parameter from given dict.
    it returns None if no offset is set in given dict.

    :param dict options: options dict to get offset from it.

    :rtype: int
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).extract_offset(options)


def enable_paging(options, offset, limit=None):
    """
    enables paging in given dict.
    it adds a paging key in given dict and sets its value to
    True. it also injects default limit and offset into it

    :param dict options: options dict to enable paging in it.
    :param int offset: offset value to be set in given dict.
    :param int limit: limit value to be set in given dict.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).enable_paging(options, offset, limit)


def disable_paging(options):
    """
    disables paging in given dict.
    it removes paging key in given dict and also
    removes keys for limit and offset.

    :param dict options: options dict to disable paging in it.
    """

    get_component(DatabasePagingPackage.COMPONENT_NAME).disable_paging(options)


def extract_paging(options):
    """
    extracts and gets limit and offset parameters from given dict.
    if limit or offset key is not available in provided
    dict, it gets the value from database config store
    from `paging` section for the absent key.

    :param dict options: options dict to get limit and offset from it.

    :returns: tuple(int limit, int offset)
    :rtype: tuple
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).extract_paging(options)


def is_paging_required(options):
    """
    gets a value indicating that paging should be done.
    it checks that paging key name is available in dict
    and its value is set to True, otherwise returns False.

    :param dict options: options dict to detect paging should be done from it.

    :rtype: bool
    """

    return get_component(DatabasePagingPackage.COMPONENT_NAME).is_paging_required(options)
