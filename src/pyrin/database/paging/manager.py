# -*- coding: utf-8 -*-
"""
database paging manager module.
"""

import pyrin.security.session.services as session_services

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
    PAGE_PARAM = 'page'
    PAGE_SIZE_PARAM = 'page_size'

    package_class = DatabasePagingPackage

    def __init__(self):
        """
        initializes an instance of DatabasePagingManager.
        """

        super().__init__()

    def extract_paging_params(self, values):
        """
        extracts paging parameters from given dict and returns them as a new dict.

        the values will be removed from input dict.

        :param dict values: a dict to extract paging params from it.

        :returns: dict(int page: page number,
                       int page_size: page size)
        :rtype: dict
        """

        page = values.pop(self.PAGE_PARAM, None)
        page_size = values.pop(self.PAGE_SIZE_PARAM, None)

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
        result[self.PAGE_PARAM] = page
        result[self.PAGE_SIZE_PARAM] = page_size
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

        return options.get(self.PAGE_PARAM), options.get(self.PAGE_SIZE_PARAM)

    def generate_paging_params(self, page, page_size):
        """
        generates paging parameters from given inputs.

        :param int page: page number.
        :param int page_size: page size.

        :returns: dict[int page, int page_size]
        :rtype: dict[int, int]
        """

        params = dict()
        params[self.PAGE_PARAM] = page
        params[self.PAGE_SIZE_PARAM] = page_size
        return params

    def inject_paging_keys(self, limit, offset, values):
        """
        injects paging keys into given dict.

        :param int limit: limit.
        :param int offset: offset.
        :param dict values: a dict to inject paging keys into it.
        """

        paging_keys = dict()
        paging_keys[self.LIMIT_KEY] = limit
        paging_keys[self.OFFSET_KEY] = offset
        values.update(paging_keys)

    def get_paging_keys(self, **options):
        """
        gets paging keys from given inputs.

        note that this method does not do any validation and just returns
        keys as they are, even if their value is None.

        :keyword int __limit__: limit value.
        :keyword int _offset__: offset value.

        :returns: tuple[int limit, int offset]
        :rtype: tuple[int, int]
        """

        return options.get(self.LIMIT_KEY), options.get(self.OFFSET_KEY)
