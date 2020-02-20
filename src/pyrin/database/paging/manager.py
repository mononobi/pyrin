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

    def __init__(self):
        """
        initializes an instance of DatabasePagingManager.
        """

        super().__init__()

        self._limit = config_services.get('database', 'paging', 'limit')
        self._offset = config_services.get('database', 'paging', 'offset')

    def get_default_limit(self):
        """
        gets default limit in database config store.

        :rtype: int
        """

        return self._limit

    def get_default_offset(self):
        """
        gets default offset in database config store.

        :rtype: int
        """

        return self._offset

    def inject_limit(self, options):
        """
        injects default limit parameter into given dict.

        :param dict options: options dict to inject limit into it.
        """

        self.inject_custom_limit(self.get_default_limit(), options)

    def inject_offset(self, options):
        """
        injects default offset parameter into given dict.

        :param dict options: options dict to inject offset into it.
        """

        self.inject_custom_offset(self.get_default_offset(), options)

    def inject_custom_limit(self, limit, options):
        """
        injects given limit parameter into given dict.

        :param int limit: limit value to be set in given dict.
        :param dict options: options dict to inject limit into it.
        """

        options.update(__limit__=limit)

    def inject_custom_offset(self, offset, options):
        """
        injects given offset parameter into given dict.

        :param int offset: offset value to be set in given dict.
        :param dict options: options dict to inject offset into it.
        """

        options.update(__offset__=offset)

    def inject_paging(self, options):
        """
        injects default limit and offset parameters into given dict.

        :param dict options: options dict to inject limit and offset into it.
        """

        self.inject_limit(options)
        self.inject_offset(options)

    def inject_custom_paging(self, limit, offset, options):
        """
        injects custom limit and offset parameters into given dict.

        :param int limit: limit value to be set in given dict.
        :param int offset: offset value to be set in given dict.
        :param dict options: options dict to inject limit and offset into it.
        """

        self.inject_custom_limit(limit, options)
        self.inject_custom_offset(offset, options)

    def extract_limit(self, options):
        """
        extracts and gets limit parameter from given dict.
        if `__limit__` key is not available in provided
        dict, it gets the value from database config store
        from `paging` section.

        :param dict options: options dict to get limit from it.

        :rtype: int
        """

        return options.get('__limit__', self.get_default_limit())

    def extract_offset(self, options):
        """
        extracts and gets offset parameter from given dict.
        if `__offset__` key is not available in provided
        dict, it gets the value from database config store
        from `paging` section.

        :param dict options: options dict to get offset from it.

        :rtype: int
        """

        return options.get('__offset__', self.get_default_offset())

    def extract_paging(self, options):
        """
        extracts and gets limit and offset parameters from given dict.
        if `__limit__` or `__offset__` key is not available in provided
        dict, it gets the value from database config store
        from `paging` section.

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
        it checks a key with name `__paging__` is available in dict
        and its value is set to True, otherwise returns False.

        :param dict options: options dict to detect paging should be done from it.

        :rtype: bool
        """

        paging = options.get('__paging__', False)
        return paging is True
