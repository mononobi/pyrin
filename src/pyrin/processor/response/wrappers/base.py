# -*- coding: utf-8 -*-
"""
response wrappers base module.
"""

from flask import Response

import pyrin.globalization.datetime.services as datetime_services
import pyrin.processor.mimetype.services as mimetype_services

from pyrin.core.structs import Context
from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.settings.static import DEFAULT_STATUS_CODE, APPLICATION_ENCODING
from pyrin.processor.exceptions import RequestIDAlreadySetError, \
    RequestDateAlreadySetError, RequestUserAlreadySetError


class CoreResponse(Response):
    """
    core response class.

    this class should be used as base for server response classes.
    """

    # charset of the response.
    charset = APPLICATION_ENCODING

    # default status if none is provided.
    default_status = DEFAULT_STATUS_CODE

    # default mimetype if none is provided.
    default_mimetype = MIMETypeEnum.TEXT

    def __init__(self, response=None, status=None,
                 headers=None, mimetype=None,
                 content_type=None, direct_passthrough=False,
                 **options):
        """
        initializes an instance of CoreResponse.

        :param str | iterable response: a string or response iterable.

        :param str | int status: a string with a status or an integer
                                 with the status code.

        :param list | Headers headers: a list of headers or a
                                       `datastructures.Headers` object.

        :param str mimetype: the mimetype for the response.
                             if not provided, it will be extracted from
                             real response value type. and if not possible,
                             it will be set to `default_mimetype`.

        :param str content_type: the content type for the response.

        :param bool direct_passthrough: if set to True the `iter_encoded` method is not
                                        called before iteration which makes it
                                        possible to pass special iterators through
                                        unchanged.
        """

        if mimetype is None:
            mimetype = self._get_mimetype(response)

        super().__init__(response, status, headers, mimetype,
                         content_type, direct_passthrough)

        self._request_id = None
        self._request_date = None
        self._response_date = datetime_services.now()
        self._user = None
        self._context = Context()

    def __str__(self):
        result = 'request id: "{request_id}", response date: "{response_date}", ' \
                 'request date: "{request_date}", user: "{user}", status_code: "{status_code}"'
        return result.format(response_date=self._response_date,
                             request_id=self._request_id,
                             request_date=self._request_date,
                             user=self._user,
                             status_code=self.status_code)

    def __hash__(self):
        return hash(self._request_id)

    def _get_mimetype(self, response):
        """
        gets the correct mimetype of given response object.

        it gets the `default_mimetype` if it fails to detect.

        :param str | iterable response: a string or response iterable.

        :returns: mimetype name
        :rtype: str
        """

        if isinstance(response, CoreResponse):
            return response.mimetype or response.default_mimetype

        mimetype = mimetype_services.get_mimetype(response)
        if mimetype is None:
            mimetype = self.default_mimetype

        return mimetype

    @property
    def request_id(self):
        """
        gets current response's request id.

        :rtype: uuid.UUID
        """

        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        sets current response's request id.

        :param uuid.UUID request_id: request id to be set.

        :raises RequestIDAlreadySetError: request id already set error.
        """

        if self._request_id is not None:
            raise RequestIDAlreadySetError('Request id for current response '
                                           'has been already set.')

        self._request_id = request_id

    @property
    def request_date(self):
        """
        gets current response's request date.

        :rtype: datetime
        """

        return self._request_date

    @request_date.setter
    def request_date(self, request_date):
        """
        sets current response's request date.

        :param datetime request_date: request date to be set.

        :raises RequestDateAlreadySetError: request date already set error.
        """

        if self._request_date is not None:
            raise RequestDateAlreadySetError('Request date for current response '
                                             'has been already set.')

        self._request_date = request_date

    @property
    def user(self):
        """
        gets current response's user.

        :rtype: object
        """

        return self._user

    @user.setter
    def user(self, user):
        """
        sets current response's user.

        :param object user: user to be set.

        :raises RequestUserAlreadySetError: request user already set error.
        """

        if self._user is not None:
            raise RequestUserAlreadySetError('Request user for current response '
                                             'has been already set.')

        self._user = user

    @property
    def context(self):
        """
        gets current response's context.

        :rtype: dict
        """

        return self._context
