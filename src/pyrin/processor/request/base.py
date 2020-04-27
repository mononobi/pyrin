# -*- coding: utf-8 -*-
"""
request base module.
"""

from flask import Request

import pyrin.utils.unique_id as uuid_utils
import pyrin.globalization.datetime.services as datetime_services
import pyrin.converters.deserializer.services as deserializer_services

from pyrin.core.structs import Context, DTO
from pyrin.settings.static import APPLICATION_ENCODING, DEFAULT_COMPONENT_KEY
from pyrin.processor.exceptions import RequestUserAlreadySetError, \
    RequestComponentCustomKeyAlreadySetError


class CoreRequest(Request):
    """
    core request class.

    this class should be used for server request.
    """

    # charset of the request.
    charset = APPLICATION_ENCODING

    def __init__(self, environ, populate_request=True,
                 shallow=False, **options):
        """
        initializes an instance of CoreRequest.

        :param environ: a wsgi environment object.
        :param bool populate_request: specifies that request should be populated.
        :param bool shallow: specifies that request should not consume form data.
        """

        super().__init__(environ, populate_request, shallow)

        self._request_id = uuid_utils.generate_uuid4()
        self._request_date = datetime_services.now()
        self._user = None
        self._component_custom_key = DEFAULT_COMPONENT_KEY
        self._client_ip = self._extract_client_ip()
        self._safe_content_length = self._extract_safe_content_length()
        self._context = Context()
        self._context.update(authorization=self._extract_authorization_header())

        # holds the inputs of request. this value will be
        # calculated once per each request and cached.
        self._inputs = None

        self._extract_locale()
        self._extract_timezone()

    def __str__(self):
        result = 'method: "{method}", route: "{route}", request id: "{request_id}", ' \
                 'request date: "{request_date}", user: "{user}", client_ip: "{client_ip}", ' \
                 'component_custom_key: "{component}"'
        return result.format(request_id=self._request_id,
                             request_date=self._request_date,
                             user=self._user,
                             client_ip=self._client_ip,
                             route=self.path,
                             method=self.method,
                             component=self._component_custom_key)

    def __hash__(self):
        return hash(self._request_id)

    def _extract_client_ip(self):
        """
        gets client ip from environ if available, otherwise returns None.

        :rtype: str
        """

        return self.environ.get('HTTP_X_REAL_IP', self.environ.get('REMOTE_ADDR', None))

    def _extract_authorization_header(self):
        """
        gets the authorization header if available, otherwise returns None.

        :rtype: str
        """

        return self.headers.get('Authorization', None)

    def get_inputs(self, silent=False):
        """
        gets request inputs.

        not that if the same keyword is available in different param
        holders, the value will be replaced and no error will be raised.
        the replacement priority is as follows:
        query_strings -> body -> view_args -> files

        for example, if a keyword named 'sample_key' is available in both body and
        query strings, the value of body will be available at the end.

        :param bool silent: specifies that if an error occurred on processing
                            json body, it should not raise an error.
                            defaults to False.

        :rtype: dict
        """

        if self._inputs is None:
            converted_args = deserializer_services.deserialize(self.args)
            self._inputs = DTO(**(converted_args or {}))
            self._inputs.update(**(self.get_json(silent=silent) or {}))
            self._inputs.update(**(self.view_args or {}))
            self._inputs.update(files=self.files)

        return self._inputs

    def _extract_safe_content_length(self):
        """
        gets content bytes length of this request if available, otherwise returns 0.

        :rtype: int
        """

        return self.content_length or 0

    def _extract_locale(self):
        """
        extracts locale name from request query params and puts it into request context.
        """

        if 'lang' in self.args.keys():
            self._context.update(locale=self.args.get('lang'))

    def _extract_timezone(self):
        """
        extracts timezone name from request query params and puts it into request context.
        """

        if 'tz' in self.args.keys():
            self._context.update(timezone=self.args.get('tz'))

    @property
    def request_id(self):
        """
        gets current request's request id.

        :rtype: uuid.UUID
        """

        return self._request_id

    @property
    def request_date(self):
        """
        gets current request's request date.

        :rtype: datetime
        """

        return self._request_date

    @property
    def user(self):
        """
        gets current request's user.

        :rtype: object
        """

        return self._user

    @user.setter
    def user(self, user):
        """
        sets current request's user.

        :param object user: user to be set.

        :raises RequestUserAlreadySetError: request user already set error.
        """

        if self._user is not None:
            raise RequestUserAlreadySetError('Request user for current request '
                                             'has been already set.')

        self._user = user

    @property
    def component_custom_key(self):
        """
        gets current request's component custom key.

        :rtype: object
        """

        return self._component_custom_key

    @component_custom_key.setter
    def component_custom_key(self, component_custom_key):
        """
        sets current request's component custom key.

        :param object component_custom_key: component custom key to be set.

        :raises RequestComponentCustomKeyAlreadySetError: request component custom
                                                          key already set error.
        """

        if self._component_custom_key != DEFAULT_COMPONENT_KEY:
            raise RequestComponentCustomKeyAlreadySetError('Request component custom key '
                                                           'for current request has been '
                                                           'already set.')

        self._component_custom_key = component_custom_key

    @property
    def client_ip(self):
        """
        gets current request's client ip if available, otherwise returns None.

        :rtype: str
        """

        return self._client_ip

    @property
    def safe_content_length(self):
        """
        gets current request's content length if available, otherwise returns 0.

        :rtype: int
        """

        return self._safe_content_length

    @property
    def context(self):
        """
        gets current request's context.

        :rtype: dict
        """

        return self._context
