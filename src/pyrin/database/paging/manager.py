# -*- coding: utf-8 -*-
"""
database paging manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.core.structs import Manager
from pyrin.database.paging import DatabasePagingPackage


class DatabasePagingManager(Manager):
    """
    database paging manager class.
    """

    # limit and offset keys that will be injected into
    # options of each view function if required.
    LIMIT_KEY = '__limit__'
    OFFSET_KEY = '__offset__'

    # paging parameters that application expects in query strings of requests.
    # these values could be customized in 'paging' section of database config store.
    PAGE_PARAM = 'page'
    PAGE_SIZE_PARAM = 'page_size'

    package_class = DatabasePagingPackage

    def __init__(self):
        """
        initializes an instance of DatabasePagingManager.
        """

        super().__init__()

        page_param = config_services.get('database', 'paging', 'page_param')
        if page_param not in (None, '') and not page_param.isspace():
            self._page_param = page_param
        else:
            self._page_param = self.PAGE_PARAM

        page_size_param = config_services.get('database', 'paging', 'page_size_param')
        if page_size_param not in (None, '') and not page_size_param.isspace():
            self._page_size_param = page_size_param
        else:
            self._page_size_param = self.PAGE_SIZE_PARAM

    def extract_paging_params(self, values):
        """
        extracts paging parameters from given dict and returns them as a new dict.

        the values will be removed from input dict.

        :param dict values: a dict to extract paging params from it.

        :returns: dict(int page: page number,
                       int page_size: page size)
        :rtype: dict
        """

        page = values.pop(self._page_param, None)
        page_size = values.pop(self._page_size_param, None)

        if isinstance(page, list):
            if len(page) > 0:
                page = page[0]
            else:
                page = None

        if isinstance(page_size, list):
            if len(page_size) > 0:
                page_size = page_size[0]
            else:
                page_size = None

        result = dict()
        result[self._page_param] = page
        result[self._page_size_param] = page_size
        return result

    def get_paging_params(self, **options):
        """
        gets paging parameters from given inputs.

        note that this method does not do any validation and just returns
        keys as they are, even if their value is None.

        :keyword int page: page number.
        :keyword int page_size: page size.

        :returns: tuple[int page, int page_size]
        :rtype: tuple[int, int]
        """

        return options.get(self._page_param), options.get(self._page_size_param)

    def generate_paging_params(self, page, page_size):
        """
        generates paging parameters from given inputs.

        :param int page: page number.
        :param int page_size: page size.

        :returns: dict[int page, int page_size]
        :rtype: dict[int, int]
        """

        params = dict()
        params[self._page_param] = page
        params[self._page_size_param] = page_size
        return params

    def inject_paging_keys(self, limit, offset, values):
        """
        injects paging keys into given dict.

        :param int limit: limit.
        :param int offset: offset.
        :param dict values: a dict to inject paging keys into it.
        """

        values[self.LIMIT_KEY] = limit
        values[self.OFFSET_KEY] = offset

    def get_paging_keys(self, **options):
        """
        gets paging keys from given inputs.

        note that this method does not do any validation and just returns
        keys as they are, even if their value is None.

        :keyword int __limit__: limit value.
        :keyword int __offset__: offset value.

        :returns: tuple[int limit, int offset]
        :rtype: tuple[int, int]
        """

        return options.get(self.LIMIT_KEY), options.get(self.OFFSET_KEY)

    def disable_paging_keys(self, values):
        """
        disables paging keys in given dict.

        :param dict values: a dict to disable paging keys in it.
        """

        self.inject_paging_keys(limit=None, offset=None, values=values)
