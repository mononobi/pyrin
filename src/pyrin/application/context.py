# -*- coding: utf-8 -*-
"""
application context module.
"""

from threading import Lock

from flask import Request, Response, jsonify

import pyrin.utils.unique_id as uuid_utils
import pyrin.globalization.datetime.services as datetime_services
import pyrin.converters.deserializer.services as deserializer_services

from pyrin.application.exceptions import ComponentAttributeError, InvalidComponentNameError
from pyrin.core.context import Context, CoreObject, DTO
from pyrin.core.exceptions import ContextAttributeError
from pyrin.settings.static import DEFAULT_STATUS_CODE, JSONIFY_MIMETYPE, \
    APPLICATION_ENCODING, DEFAULT_COMPONENT_KEY
from pyrin.utils.singleton import UniqueSingletonMeta


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

        # component id is a tuple(str, object) and should be unique for each
        # instance unless it's intended to replace an already existing one.
        self._component_id = self.make_component_id(component_name, **options)

    def get_id(self):
        """
        gets the component id of this instance.

        :rtype: tuple(str, object)
        """

        return self._component_id

    @staticmethod
    def make_component_id(component_name, **options):
        """
        makes a component id based on input values and returns it.

        :param str component_name: component name.

        :keyword object component_custom_key: component custom key.

        :raises InvalidComponentNameError: invalid component name.

        :rtype: tuple(str, object)
        """

        if component_name is None or len(component_name.strip()) <= 0:
            raise InvalidComponentNameError('Component name should not be None.')

        component_custom_key = options.get('component_custom_key', DEFAULT_COMPONENT_KEY)
        return component_name, component_custom_key


class CoreResponse(Response):
    """
    represents base response.
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
        super().__init__(response, **kwargs)

        self.request_id = None
        self.request_date = None
        self.response_date = datetime_services.now()
        self.user = None
        self.context = Context()

    @classmethod
    def force_type(cls, response, environ=None):
        response = cls.response_converter(response)
        return super().force_type(response, environ)

    def __str__(self):
        result = 'request id: "{request_id}", response date: "{response_date}", ' \
                 'request date: "{request_date}", user: "{user}", status_code: "{status_code}"'
        return result.format(response_date=self.response_date,
                             request_id=self.request_id,
                             request_date=self.request_date,
                             user=self.user,
                             status_code=self.status_code)

    def __hash__(self):
        return hash(self.request_id)


class CoreRequest(Request):
    """
    represents base request class.
    this class should be used for server request.
    """

    # charset of the request.
    charset = APPLICATION_ENCODING

    def __init__(self, environ, populate_request=True,
                 shallow=False, **options):
        super().__init__(environ, populate_request, shallow)

        self.request_id = uuid_utils.generate_uuid4()
        self.request_date = datetime_services.now()
        self.user = None
        self.component_custom_key = DEFAULT_COMPONENT_KEY
        self.client_ip = self._get_client_ip()
        self.safe_content_length = self._get_safe_content_length()
        self.context = Context()
        self.context.update(authorization=self._get_authorization_header())

        # holds the inputs of request. this value will be
        # calculated once per each request and cached.
        self.__inputs = None

        self._extract_locale()
        self._extract_timezone()

    def __str__(self):
        result = 'method: "{method}", route: "{route}", request id: "{request_id}", ' \
                 'request date: "{request_date}", user: "{user}", client_ip: "{client_ip}", ' \
                 'component_custom_key: "{component}"'
        return result.format(request_id=self.request_id,
                             request_date=self.request_date,
                             user=self.user,
                             client_ip=self.client_ip,
                             route=self.path,
                             method=self.method,
                             component=self.component_custom_key)

    def __hash__(self):
        return hash(self.request_id)

    def _get_client_ip(self):
        """
        gets client ip from request if available.

        :rtype: str
        """

        return self.environ.get('HTTP_X_REAL_IP', self.environ.get('REMOTE_ADDR', None))

    def _get_authorization_header(self):
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
        query_strings, the value of body will be available at the end.

        :param bool silent: specifies that if an error occurred on processing
                            json body, it should not raise an error.
                            defaults to False.

        :rtype: dict
        """

        if self.__inputs is None:
            converted_args = deserializer_services.deserialize(self.args)
            self.__inputs = DTO(**(converted_args or {}))
            self.__inputs.update(**(self.get_json(silent=silent) or {}))
            self.__inputs.update(**(self.view_args or {}))
            self.__inputs.update(files=self.files)

        return self.__inputs

    def _get_safe_content_length(self):
        """
        gets content bytes length of this request if available.
        otherwise returns 0.

        :rtype: int
        """

        return self.content_length or 0

    def _extract_locale(self):
        """
        extracts locale name from request query params and puts it into request context.
        """

        if 'lang' in self.args.keys():
            self.context.update(locale=self.args.get('lang'))

    def _extract_timezone(self):
        """
        extracts timezone name from request query params and puts it into request context.
        """

        if 'tz' in self.args.keys():
            self.context.update(timezone=self.args.get('tz'))


class ApplicationSingletonMeta(UniqueSingletonMeta):
    """
    application singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    instance = None
    _lock = Lock()
