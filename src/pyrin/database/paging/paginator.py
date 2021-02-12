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
from pyrin.database.paging.exceptions import PageSizeLimitError, TotalCountIsAlreadySetError


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

    @abstractmethod
    def has_next(self, count, *args, **options):
        """
        gets a value indicating that there is a next page available.

        it returns a tuple of two items. first item is a boolean indicating
        that there is a next page and the second item is the number of excess
        items that must be removed from end of items.

        :param int count: count of current items.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: tuple[bool has_next, int excess]
        :rtype: tuple[bool, int]
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def has_previous(self, count, *args, **options):
        """
        gets a value indicating that there is a previous page available.

        it returns a tuple of two items. first item is a boolean indicating
        that there is a previous page and the second item is the number of
        excess items that must be removed from beginning of items.

        :param int count: count of current items.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: tuple[bool has_previous, int excess]
        :rtype: tuple[bool, int]
        """

        raise CoreNotImplementedError()

    def copy(self):
        """
        returns a deep copy of this instance

        :rtype: PaginatorBase
        """

        return deepcopy(self)

    @property
    @abstractmethod
    def current_page(self):
        """
        gets current page number.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def current_page_size(self):
        """
        gets current page size.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def total_count(self):
        """
        gets the total count of items in all pages.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @total_count.setter
    @abstractmethod
    def total_count(self, value):
        """
        sets the total count of items in all pages.

        :param int value: total count to be set.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()


class SimplePaginator(PaginatorBase):
    """
    simple paginator class.

    page numbers start from 1.
    it does not emit any extra queries to database to fetch count or like that.
    the only limitation is that it could not detect previous page from the
    `last_page + 1` page.
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
        self._has_previous = False
        self._total_count = None

    def _url_for(self, page, page_size):
        """
        gets the url for given page number.

        :param int page: page number to generate its url.
        :param int page_size: page size.

        :rtype: str
        """

        request = session_services.get_current_request()
        options = OrderedDict()
        options.update(paging_services.generate_paging_params(page, page_size))
        options.update(request.get_all_query_strings())
        return url_for(self._endpoint, **options)

    def has_next(self, count, **options):
        """
        gets a value indicating that there is a next page available.

        it returns a tuple of two items. first item is a boolean indicating
        that there is a next page and the second item is the number of excess
        items that must be removed from end of items.

        :param int count: count of current items.

        :returns: tuple[bool has_next, int excess]
        :rtype: tuple[bool, int]
        """

        # the original limit is always 2 less than the current limit.
        excess = count - (self._limit - 2)
        if excess <= 0:
            self._has_next = False
            return self._has_next, 0

        if self._current_page == 1:
            self._has_next = excess > 0
            return self._has_next, excess
        else:
            self._has_next = excess > 1
            return self._has_next, excess - 1

    def has_previous(self, count, **options):
        """
        gets a value indicating that there is a previous page available.

        it returns a tuple of two items. first item is a boolean indicating
        that there is a previous page and the second item is the number of
        excess items that must be removed from beginning of items.

        :param int count: count of current items.

        :returns: tuple[bool has_previous, int excess]
        :rtype: tuple[bool, int]
        """

        # at any page, if there is a count > 0, it means that there is a previous
        # page available. because the first item is from the previous page.
        if count <= 0 or self._current_page == 1:
            self._has_previous = False
            return self._has_previous, 0

        self._has_previous = True
        return self._has_previous, 1

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

        if self._has_previous is True:
            return self._url_for(self._current_page - 1, self._current_page_size)

        return None

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

        # we increase limit by 2 to be able to detect if there is a next and previous page.
        # the extra items will not be returned to client.
        self._limit = page_size + 2
        offset = page - 1
        extra_offset = offset * page_size
        if extra_offset > 0:
            # we decrease offset by 1 to be able to detect if there is a previous page.
            # the extra item will not be returned to client.
            extra_offset = extra_offset - 1

        self._offset = extra_offset
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
        count = len(items)
        result = items

        has_next, excess_end = self.has_next(count)
        has_previous, excess_first = self.has_previous(count)
        if has_next is True:
            result = result[:-excess_end]
            count = count - excess_end

        if has_previous is True:
            result = result[excess_first:]
            count = count - excess_first

        next_url = self.next()
        previous_url = self.previous()

        if self.total_count is not None:
            metadata.update(count_total=self.total_count)

        metadata.update(count=count, next=next_url, previous=previous_url)
        return result, metadata

    @property
    def current_page(self):
        """
        gets current page number.

        :rtype: int
        """

        return self._current_page

    @property
    def current_page_size(self):
        """
        gets current page size.

        :rtype: int
        """

        return self._current_page_size

    @property
    def total_count(self):
        """
        gets the total count of items in all pages.

        :rtype: int
        """

        return self._total_count

    @total_count.setter
    def total_count(self, value):
        """
        sets the total count of items in all pages.

        :param int value: total count to be set.

        :raises TotalCountIsAlreadySetError: total count is already set error.
        """

        if self._total_count is not None:
            raise TotalCountIsAlreadySetError('Total count for paginator is already '
                                              'set and could not be overwritten in '
                                              'current request.')

        self._total_count = value
