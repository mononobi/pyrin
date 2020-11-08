# -*- coding: utf-8 -*-
"""
response wrappers base module.
"""

from flask import Response
from werkzeug.test import run_wsgi_app

import pyrin.globalization.datetime.services as datetime_services
import pyrin.processor.mimetype.services as mimetype_services

from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.processor.response.wrappers.structs import ResponseContext
from pyrin.settings.static import DEFAULT_STATUS_CODE, APPLICATION_ENCODING
from pyrin.processor.response.wrappers.exceptions import InvalidResponseContextKeyNameError, \
    ResponseContextKeyIsAlreadyPresentError, ResponseEnvironRequiredError
from pyrin.processor.exceptions import RequestIDAlreadySetError, \
    RequestDateAlreadySetError, RequestUserAlreadySetError


class CoreResponse(Response):
    """
    core response class.

    this class should be used as base for server response classes.
    """

    # charset of the response.
    charset = APPLICATION_ENCODING

    # class to be used as response context holder.
    response_context_class = ResponseContext

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

        :keyword dict original_data: a dict containing the original
                                     data of response before encoding.
                                     this value will be used in logging
                                     to mask critical values.
        """

        if mimetype is None:
            mimetype = self._get_mimetype(response)

        super().__init__(response, status, headers, mimetype,
                         content_type, direct_passthrough)

        self._original_data = None
        self.original_data = options.get('original_data')
        self._request_id = None
        self._request_date = None
        self._response_date = datetime_services.now()
        self._user = None
        self._context = self.response_context_class()

    def __str__(self):
        result = 'request id: "{request_id}", request date: "{request_date}", ' \
                 'response date: "{response_date}", user: "{user}", ' \
                 'status_code: "{status_code}"'
        return result.format(response_date=self._response_date,
                             request_id=self.request_id,
                             request_date=self.request_date,
                             user=self.user,
                             status_code=self.status_code)

    def __hash__(self):
        return hash(self.request_id)

    def _get_mimetype(self, response):
        """
        gets the correct mimetype of given response object.

        it gets the `default_mimetype` if it fails to detect.

        :param str | iterable response: a string or response iterable.

        :returns: mimetype name
        :rtype: str
        """

        mimetype = mimetype_services.get_mimetype(response)
        if mimetype is None:
            mimetype = self.default_mimetype

        return mimetype

    def add_context(self, key, value, **options):
        """
        adds the given key/value pair into current response context.

        :param str key: key name to be added.
        :param object value: value to be added.

        :keyword bool replace: specifies that if a key with the same name
                               is already present, replace it. otherwise
                               raise an error. defaults to False if not provided.

        :raises InvalidResponseContextKeyNameError: invalid response context key name error.
        :raises ResponseContextKeyIsAlreadyPresentError: response context key is
                                                         already present error.
        """

        if key in (None, '') or key.isspace():
            raise InvalidResponseContextKeyNameError('Response context key must be provided.')

        if key in self._context:
            replace = options.get('replace', None)
            if replace is None:
                replace = False

            if replace is not True:
                raise ResponseContextKeyIsAlreadyPresentError('A response context with key '
                                                              '[{key}] is already present '
                                                              'and "replace" option is not set.'
                                                              .format(key=key))
        self._context[key] = value

    def get_context(self, key, default=None):
        """
        gets the value for given key from current response context.

        it gets the default value if key is not present in the response context.

        :param str key: key name to get its value.
        :param object default: a value to be returned if the provided
                               key is not present in response context.

        :rtype: object
        """

        return self._context.get(key, default)

    def remove_context(self, key):
        """
        removes the specified key from current response context if available.

        :param str key: key name to be removed from response context.
        """

        self._context.pop(key, None)

    @classmethod
    def force_type(cls, response, environ=None):
        """
        enforces that the wsgi response is a response object of the current type.

        this method can enforce a given response type, and it will also
        convert arbitrary wsgi callables into response objects if an environ
        is provided.

        this is especially useful if you want to post-process responses in
        the main dispatcher and use functionality provided by your subclass.

        keep in mind that this will modify response objects in place if
        possible.

        :param object response: a response object or wsgi application.
        :param dict environ: a wsgi environment object.

        :raises ResponseEnvironRequiredError: response environ required error.

        :returns: a response object.
        :rtype: CoreResponse
        """

        if not isinstance(response, CoreResponse):
            if environ is None:
                raise ResponseEnvironRequiredError('Cannot convert WSGI application into '
                                                   'response object without an environ.')

            response = CoreResponse(*run_wsgi_app(response, environ))

        response.__class__ = cls
        return response

    @property
    def safe_content_length(self):
        """
        gets current response's content length if available, otherwise returns 0.

        :rtype: int
        """

        return self.content_length or 0

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
    def original_data(self):
        """
        gets the original data of this response.

        it returns a dict if the original data was a dict, otherwise
        it gets the response data as text.

        :rtype: dict | str
        """

        return self._original_data or self.get_data(as_text=True)

    @original_data.setter
    def original_data(self, data):
        """
        sets the response original data if it is of dict type.

        otherwise sets None for this value.
        this value will be used for response logging to let loggers mask critical values.

        :param dict data: data to be registered.
        """

        if isinstance(data, dict):
            self._original_data = dict(data)
