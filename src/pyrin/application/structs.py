# -*- coding: utf-8 -*-
"""
application structs module.
"""

from threading import Lock

from flask import Request, Response, jsonify

import pyrin.utils.unique_id as uuid_utils
import pyrin.globalization.datetime.services as datetime_services
import pyrin.converters.deserializer.services as deserializer_services

from pyrin.core.structs import Context, CoreObject, DTO, UniqueSingletonMeta
from pyrin.core.exceptions import ContextAttributeError
from pyrin.settings.static import DEFAULT_STATUS_CODE, JSONIFY_MIMETYPE, \
    APPLICATION_ENCODING, DEFAULT_COMPONENT_KEY
from pyrin.application.exceptions import ComponentAttributeError, InvalidComponentNameError, \
    RequestIDAlreadySetError, RequestDateAlreadySetError, RequestUserAlreadySetError, \
    RequestComponentCustomKeyAlreadySetError


class ApplicationContext(Context):
    """
    context class to hold application contextual data.
    """

    def _raise_key_error(self, key):
        """
        raises an error for given key.

        :param object key: key object that caused the error.

        :raises ContextAttributeError: context attribute error.
        """

        raise ContextAttributeError('Property [{name}] not found in application context.'
                                    .format(name=key))


class ApplicationComponent(ApplicationContext):
    """
    context class to hold application components.
    """

    def _raise_key_error(self, key):
        """
        raises an error for given key.

        :param object key: key object that caused the error.

        :raises ComponentAttributeError: component attribute error.
        """

        raise ComponentAttributeError('Component [{name}] is not available '
                                      'in application components.'.format(name=key))


class Component(CoreObject):
    """
    base component class.

    all component classes must inherit from this class and their respective manager class.
    """

    def __init__(self, component_name, **options):
        """
        initializes an instance of Component.

        :param str component_name: component name.

        :keyword object component_custom_key: component custom key.
        """

        super().__init__()

        # component id is a tuple[str, object] and should be unique for each
        # instance unless it's intended to replace an already existing one.
        self._component_id = self.make_component_id(component_name, **options)

    def get_id(self):
        """
        gets the component id of this instance.

        :rtype: tuple[str, object]
        """

        return self._component_id

    @staticmethod
    def make_component_id(component_name, **options):
        """
        makes a component id based on input values and returns it.

        :param str component_name: component name.

        :keyword object component_custom_key: component custom key.

        :raises InvalidComponentNameError: invalid component name.

        :rtype: tuple[str, object]
        """

        if component_name is None or len(component_name.strip()) <= 0:
            raise InvalidComponentNameError('Component name should not be None.')

        component_custom_key = options.get('component_custom_key', DEFAULT_COMPONENT_KEY)
        return component_name, component_custom_key


class CoreResponse(Response):
    """
    core response class.

    this class should be used as server response.
    """

    # charset of the response.
    charset = APPLICATION_ENCODING

    # default status if none is provided.
    default_status = DEFAULT_STATUS_CODE

    # default mimetype if none is provided.
    default_mimetype = JSONIFY_MIMETYPE

    # function to use as response converter.
    response_converter = jsonify

    def __init__(self, response=None, **kwargs):
        """
        initializes an instance of CoreResponse.

        :param str | iterable response: a string or response iterable.
        """

        super().__init__(response, **kwargs)

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

    @classmethod
    def force_type(cls, response, environ=None):
        """
        enforce that the wsgi response is a response object of the current type.

        :param object response: response object.

        :param environ: a wsgi environment object.

        :rtype: CoreResponse
        """

        response = cls.response_converter(response)
        return super().force_type(response, environ)

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


class ApplicationSingletonMeta(UniqueSingletonMeta):
    """
    application singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    instance = None
    _lock = Lock()
