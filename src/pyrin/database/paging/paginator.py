# -*- coding: utf-8 -*-
"""
database paging paginator module.
"""

from copy import deepcopy
from abc import abstractmethod
from collections import OrderedDict

from flask import url_for

import pyrin.configuration.services as config_services
import pyrin.database.paging.services as paging_services
import pyrin.security.session.services as session_services

from pyrin.core.structs import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.paging.exceptions import PageSizeLimitError


class PaginatorBase(CoreObject):
    """
    paginator base class.
    """

    @abstractmethod
    def next(self):
        """
        gets the next page number.

        returns None if there is no next page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def previous(self):
        """
        gets the previous page number.

        returns None if there is no previous page.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def inject_paging_keys(self, values, **options):
        """
        injects paging keys into given values from given inputs.

        :param dict values: dict values to inject paging keys into it.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def paginate(self, items, **options):
        """
        paginates the given items.

        it returns a tuple of two values, first value is a list of items
        to be returned to client, and second value is a dict of metadata
        to be injected into client response.

        :param list items: items to be paginated.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: tuple[list items, dict metadata]
        :rtype: tuple[list, dict]
        """

        raise CoreNotImplementedError()

    def has_next(self):
        """
        gets a value indicating that there is a next page available.

        :rtype: bool
        """

        return self.next() is not None

    def has_previous(self):
        """
        gets a value indicating that there is a previous page available.

        :rtype: bool
        """

        return self.previous() is not None

    def copy(self):
        """
        returns a deep copy of this instance

        :rtype: PaginatorBase
        """

        return deepcopy(self)


class SimplePaginator(PaginatorBase):
    """
    simple paginator class.

    page numbers start from 1.
    """

    def __init__(self, endpoint, **options):
        """
        initializes an instance of SimplePaginator.

        :param str endpoint: endpoint of route.

        :keyword int page_size: default page size.
                                if not provided, it will be get from
                                `default_page_size` of `database` config store.

        :keyword int max_page_size: max allowed page size.
                                    if not provided, it will be get from
                                    `max_page_size` of `database` config store.

        :raises PageSizeLimitError: page size limit error.
        """

        super().__init__()

        global_max_page_size = config_services.get('database', 'paging', 'max_page_size')
        max_page_size = options.get('max_page_size')
        if max_page_size is None or max_page_size < 1:
            max_page_size = global_max_page_size

        if max_page_size > global_max_page_size:
            raise PageSizeLimitError('Max page size [{max}] is bigger than global max page '
                                     'size which is [{global_max}] on endpoint [{endpoint}].'
                                     .format(max=max_page_size,
                                             global_max=global_max_page_size,
                                             endpoint=endpoint))

        page_size = options.get('page_size')
        default_page_size = config_services.get('database', 'paging', 'default_page_size')
        if page_size is None or page_size < 1:
            page_size = min(default_page_size, max_page_size)

        if page_size > max_page_size:
            raise PageSizeLimitError('Page size [{page_size}] is bigger than max page size '
                                     'which is [{max}] on endpoint [{endpoint}].'
                                     .format(page_size=page_size,
                                             max=max_page_size,
                                             endpoint=endpoint))

        self._page_size = page_size
        self._max_page_size = max_page_size
        self._endpoint = endpoint
        self._limit = None
        self._offset = None
        self._current_page = None
        self._current_page_size = None
        self._has_next = False

    def _url_for(self, page, page_size):
        """
        gets the url for give page number.

        :param int page: page number to generate its url.
        :param int page_size: page size.

        :rtype: str
        """

        request = session_services.get_current_request()
        options = OrderedDict()
        options.update(paging_services.generate_paging_params(page, page_size))
        options.update(request.get_all_query_strings())
        return url_for(self._endpoint, **options)

    def next(self):
        """
        gets the next page number.

        returns None if there is no next page.

        :rtype: int
        """

        if self._has_next is True:
            return self._url_for(self._current_page + 1, self._current_page_size)

        return None

    def previous(self):
        """
        gets the previous page number.

        returns None if there is no previous page.

        :rtype: int
        """

        if self._current_page <= 1:
            return None
        else:
            return self._url_for(self._current_page - 1, self._current_page_size)

    def inject_paging_keys(self, values, **options):
        """
        injects paging keys into given values from given inputs.

        :param dict values: dict values to inject paging keys into it.

        :keyword int page: page number.
        :keyword int page_size: page size.
        """

        page, page_size = paging_services.get_paging_params(**options)

        if page is None or not isinstance(page, int) or page < 1:
            page = 1

        if page_size is None or not isinstance(page_size, int) or page_size < 1:
            page_size = self._page_size
        elif page_size > self._max_page_size:
            page_size = self._max_page_size

        # we increase limit by 1 to be able to detect if there is a next page.
        # the extra item will not be returned to client.
        self._limit = page_size + 1
        offset = page - 1
        self._offset = offset * page_size
        self._current_page = page
        self._current_page_size = page_size
        paging_services.inject_paging_keys(self._limit, self._offset, values)

    def paginate(self, items, **options):
        """
        paginates the given items.

        it returns a tuple of two values, first value is a list of items
        to be returned to client, and second value is a dict of metadata
        to be injected into client response.

        :param list items: items to be paginated.

        :returns: tuple[list items, dict metadata]
        :rtype: tuple[list, dict]
        """

        metadata = OrderedDict()
        length = len(items)
        count = length
        result = items

        if length >= self._limit:
            result = items[:-1]
            count = count - 1
            self._has_next = True

        next_url = self.next()
        previous_url = self.previous()
        metadata.update(count=count, next=next_url, previous=previous_url)
        return result, metadata
