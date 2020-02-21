# -*- coding: utf-8 -*-
"""
database paging manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.core.context import Manager


class DatabasePagingManager(Manager):
    """
    database paging manager class.
    """

    PAGING_KEY = '__paging__'
    LIMIT_KEY = '__limit__'
    OFFSET_KEY = '__offset__'

    def __init__(self):
        """
        initializes an instance of DatabasePagingManager.
        """

        super().__init__()

        self._limit = config_services.get('database', 'paging', 'limit')
        self._auto = config_services.get('database', 'paging', 'auto')

    def get_default_limit(self):
        """
        gets default limit from database config store.

        :rtype: int
        """

        return self._limit

    def is_auto_paging(self):
        """
        gets a value indicating that auto paging is enabled.

        :rtype: bool
        """

        return self._auto

    def enable_limit(self, options, limit=None):
        """
        enables limit with default or given limit parameter in given dict.

        :param int limit: custom limit value to be injected into given dict.
                          if not provided, defaults to limit value in
                          database config store.

        :param dict options: options dict to inject limit in it.
        """

        if limit is None:
            limit = self.get_default_limit()

        options[self.LIMIT_KEY] = limit

    def _enable_offset(self, options, offset):
        """
        enables offset with given value in input dict.

        :param int offset: offset value that should be injected into given dict.

        :param dict options: options dict to enable offset in it.
        """

        options[self.OFFSET_KEY] = offset

    def disable_limit(self, options):
        """
        disables limit in given dict. it removes limit key from it.

        :param dict options: options dict to disable limit in it.
        """

        options.pop(self.LIMIT_KEY, None)

    def _disable_offset(self, options):
        """
        disables offset in given dict. it removes offset key from it.

        :param dict options: options dict to disable offset in it.
        """

        options.pop(self.OFFSET_KEY, None)

    def extract_limit(self, options):
        """
        extracts and gets limit parameter from given dict.
        it returns None if no limit is set in given dict.

        :param dict options: options dict to get limit from it.

        :rtype: int
        """

        return options.get(self.LIMIT_KEY, None)

    def extract_offset(self, options):
        """
        extracts and gets offset parameter from given dict.
        it returns None if no offset is set in given dict.

        :param dict options: options dict to get offset from it.

        :rtype: int
        """

        return options.get(self.OFFSET_KEY, None)

    def enable_paging(self, options, offset, limit=None):
        """
        enables paging in given dict.
        it adds a paging key in given dict and sets its value to
        True. it also injects default limit and offset into it

        :param dict options: options dict to enable paging in it.
        :param int offset: offset value to be set in given dict.
        :param int limit: limit value to be set in given dict.
        """

        options[self.PAGING_KEY] = True
        self.enable_limit(options, limit)
        self._enable_offset(options, offset)

    def disable_paging(self, options):
        """
        disables paging in given dict.
        it removes paging key in given dict and also
        removes keys for limit and offset.

        :param dict options: options dict to disable paging in it.
        """

        options.pop(self.PAGING_KEY, None)
        self.disable_limit(options)
        self._disable_offset(options)

    def extract_paging(self, options):
        """
        extracts and gets limit and offset parameters from given dict.
        if limit or offset key is not available in provided
        dict, it gets the value from database config store
        from `paging` section for the absent key.

        :param dict options: options dict to get limit and offset from it.

        :returns: tuple(int limit, int offset)
        :rtype: tuple
        """

        limit = self.extract_limit(options)
        offset = self.extract_offset(options)

        return limit, offset

    def is_paging_required(self, options):
        """
        gets a value indicating that paging should be done.
        it checks that paging key name is available in dict
        and its value is set to True, otherwise returns False.

        :param dict options: options dict to detect paging should be done from it.

        :rtype: bool
        """

        paging = options.get(self.PAGING_KEY, False)
        return paging is True
