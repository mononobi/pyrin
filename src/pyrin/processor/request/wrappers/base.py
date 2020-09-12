# -*- coding: utf-8 -*-
"""
request wrappers base module.
"""

from flask import Request

import pyrin.utils.unique_id as uuid_utils
import pyrin.globalization.datetime.services as datetime_services
import pyrin.converters.deserializer.services as deserializer_services
import pyrin.configuration.services as config_services

from pyrin.core.globals import _
from pyrin.caching.structs import CacheableDict
from pyrin.core.structs import DTO, CoreImmutableMultiDict
from pyrin.processor.request.wrappers.structs import RequestContext
from pyrin.settings.static import APPLICATION_ENCODING, DEFAULT_COMPONENT_KEY
from pyrin.processor.exceptions import RequestUserAlreadySetError, \
    RequestComponentCustomKeyAlreadySetError
from pyrin.processor.request.wrappers.exceptions import InvalidRequestContextKeyNameError, \
    RequestContextKeyIsAlreadyPresentError, BadRequestError, \
    BothRequestBodyAndFormDataProvidedError, JSONBodyDecodingError, BodyDecodingError


class CoreRequest(Request):
    """
    core request class.

    this class should be used for server request.
    """

    # charset of the request.
    charset = APPLICATION_ENCODING

    # class to be used as request context holder.
    request_context_class = RequestContext

    # class to be used for 'args' and 'form' data.
    parameter_storage_class = CoreImmutableMultiDict

    # class to be used for dict values from the incoming WSGI.
    dict_storage_class = CoreImmutableMultiDict

    # these are query param names that application expects for locale and timezone.
    LOCALE_PARAM_NAME = 'lang'
    TIMEZONE_PARAM_NAME = 'tz'

    # application expects an authorization header in request with this key.
    AUTHORIZATION_HEADER_KEY = 'Authorization'

    # application expects one of these keys in environ dict to get client ip from.
    CLIENT_IP_ENVIRON_KEY_1 = 'HTTP_X_REAL_IP'
    CLIENT_IP_ENVIRON_KEY_2 = 'REMOTE_ADDR'

    # these are the keys that application will use to store
    # locale and timezone in them and put inside request context.
    LOCALE_CONTEXT_KEY = 'locale'
    TIMEZONE_CONTEXT_KEY = 'timezone'

    # application will store authorization header in request context with this key.
    AUTHORIZATION_CONTEXT_KEY = 'authorization'

    def __init__(self, environ, populate_request=True,
                 shallow=False, **options):
        """
        initializes an instance of CoreRequest.

        :param dict environ: a wsgi environment object.
        :param bool populate_request: specifies that request should be populated.
        :param bool shallow: specifies that request should not consume form data.
        """

        super().__init__(environ, populate_request, shallow)

        self._request_id = uuid_utils.generate_uuid4()
        self._request_date = datetime_services.now()
        self._user = None
        self._cacheable_user = None
        self._component_custom_key = DEFAULT_COMPONENT_KEY
        self._client_ip = self._get_client_ip()
        self._safe_content_length = self._get_safe_content_length()
        self._context = self.request_context_class()

        # holds the inputs of request. this value will be
        # calculated once per each request and cached.
        self._inputs = None

        self._extract_authorization_header()
        self._extract_locale()
        self._extract_timezone()

        # this holds any exception that might be raised on body decoding.
        # when silent is not passed to 'get_inputs' method, if this value
        # is not None, it will be raised.
        self._body_decoding_error = None

    def __str__(self):
        result = 'request id: "{request_id}", request date: "{request_date}", ' \
                 'user: "{user}", method: "{method}", route: "{route}", ' \
                 'endpoint: "{endpoint}", client_ip: "{client_ip}", ' \
                 'component_custom_key: "{component}"'
        return result.format(request_id=self.request_id,
                             request_date=self.request_date,
                             user=self.user,
                             client_ip=self.client_ip,
                             route=self.path,
                             method=self.method,
                             endpoint=self._get_endpoint(),
                             component=self.component_custom_key)

    def __hash__(self):
        return hash(self.request_id)

    def _get_endpoint(self):
        """
        gets the endpoint if available.

        otherwise return None.

        :rtype: str
        """

        if self.url_rule is not None:
            return self.url_rule.endpoint

        return None

    def _get_client_ip(self):
        """
        gets client ip from environ if available, otherwise returns None.

        :rtype: str
        """

        return self.environ.get(self.CLIENT_IP_ENVIRON_KEY_1,
                                self.environ.get(self.CLIENT_IP_ENVIRON_KEY_2, None))

    def _extract_authorization_header(self):
        """
        extracts authorization header if available and puts it into
        request context, otherwise puts None into request context.
        """

        self.add_context(self.AUTHORIZATION_CONTEXT_KEY,
                         self.headers.get(self.AUTHORIZATION_HEADER_KEY, None))

    def _remove_extra_query_params(self, params):
        """
        removes all kwargs that should not be handed to the view function directly.

        for example `LOCALE_PARAM_NAME` and `TIMEZONE_PARAM_NAME` will be removed
        from query params because they will be stored in request context.
        this method removes extra kwargs from input dict directly and does
        not return anything.

        :param dict params: a dict containing all query params.
        """

        params.pop(self.LOCALE_PARAM_NAME, None)
        params.pop(self.TIMEZONE_PARAM_NAME, None)

    def _get_safe_content_length(self):
        """
        gets content bytes length of this request if available, otherwise returns 0.

        :rtype: int
        """

        return self.content_length or 0

    def _extract_locale(self):
        """
        extracts locale name from request query params and puts it into request context.
        """

        self.add_context(self.LOCALE_CONTEXT_KEY,
                         self.args.get(self.LOCALE_PARAM_NAME, None))

    def _extract_timezone(self):
        """
        extracts timezone name from request query params and puts it into request context.
        """

        self.add_context(self.TIMEZONE_CONTEXT_KEY,
                         self.args.get(self.TIMEZONE_PARAM_NAME, None))

    def get_body(self, silent=False):
        """
        gets data from request body.

        this method gets body as a dict if it is a json data.
        otherwise it returns an empty dict.

        :param bool silent: specifies that if an error occurred on processing
                            request body, it should not raise an error.
                            defaults to False.

        :raises BadRequestError: bad request error.

        :rtype: dict
        """

        if self.is_json is True:
            try:
                return self.get_json(silent=False) or {}
            except Exception as json_error:
                if silent is not True:
                    raise
                self._body_decoding_error = json_error
                return {}

        try:
            return self._get_custom_body() or {}
        except Exception as body_error:
            if silent is not True:
                self.on_body_loading_failed(error=body_error)
            self._body_decoding_error = body_error
            return {}

    def _get_custom_body(self):
        """
        gets data from a custom format request body.

        this method is intended to be overridden by subclasses.
        they must return an empty dict if could not convert the body.

        :rtype: dict
        """

        return {}

    def get_inputs(self, silent=False):
        """
        gets request inputs.

        not that if the same keyword is available in different param
        holders, the value will be replaced and no error will be raised.
        the replacement priority is as follows:
        [query_strings] -> [body or form_data] -> [view_args] -> [uploaded_files]

        for example, if a keyword named 'sample_key' is available in both body and
        query strings, the value of body will be available at the end.

        note that in the context of http requests, it is not possible for a
        request to have both body and form data at the same time. so this method
        will raise an error in such scenario.

        :param bool silent: specifies that if an error occurred on processing
                            request body, it should not raise an error.
                            defaults to False.

        :raises JSONBodyDecodingError: json body decoding error.
        :raises BodyDecodingError: body decoding error.
        :raises BothRequestBodyAndFormDataProvidedError: both request body and
                                                         form data provided error.

        :rtype: dict
        """

        if silent is not True and self._body_decoding_error is not None:
            raise self._body_decoding_error

        if self._inputs is None:
            query_strings = deserializer_services.deserialize(self.args.to_dict(flat=False,
                                                                                all_list=False))
            form_data = deserializer_services.deserialize(self.form.to_dict(flat=False,
                                                                            all_list=False))
            body = self.get_body(silent=silent)

            if len(body) > 0 and len(form_data) > 0:
                error = BothRequestBodyAndFormDataProvidedError(_('Request could not contain '
                                                                  'both body and form data at '
                                                                  'the same time.'))
                if silent is not True:
                    raise error
                self._body_decoding_error = error

            self._remove_extra_query_params(query_strings)
            self._inputs = DTO(query_strings)
            self._inputs.update(body)
            self._inputs.update(form_data)
            self._inputs.update(self.view_args or {})

            if self.files is not None and len(self.files) > 0:
                self._inputs.update(uploaded_files=self.files.to_dict(flat=False,
                                                                      all_list=False))

        return self._inputs

    def add_context(self, key, value, **options):
        """
        adds the given key/value pair into current request context.

        :param str key: key name to be added.
        :param object value: value to be added.

        :keyword bool replace: specifies that if a key with the same name
                               is already present, replace it. otherwise
                               raise an error. defaults to False if not provided.

        :raises InvalidRequestContextKeyNameError: invalid request context key name error.
        :raises RequestContextKeyIsAlreadyPresentError: request context key is
                                                        already present error.
        """

        if key in (None, '') or key.isspace():
            raise InvalidRequestContextKeyNameError('Request context key must be provided.')

        if key in self._context:
            replace = options.get('replace', None)
            if replace is None:
                replace = False

            if replace is not True:
                raise RequestContextKeyIsAlreadyPresentError('A request context with key '
                                                             '[{key}] is already present '
                                                             'and "replace" option is not set.'
                                                             .format(key=key))
        self._context[key] = value

    def get_context(self, key, default=None):
        """
        gets the value for given key from current request context.

        it gets the default value if key is not present in the request context.

        :param str key: key name to get its value.
        :param object default: a value to be returned if the provided
                               key is not present in request context.

        :rtype: object
        """

        return self._context.get(key, default)

    def remove_context(self, key):
        """
        removes the specified key from current request context if available.

        :param str key: key name to be removed from request context.
        """

        self._context.pop(key, None)

    def on_json_loading_failed(self, error):
        """
        raises an error on json loading failure.

        :param Exception error: exception that occurred on loading the json body.

        :raises JSONBodyDecodingError: json body decoding error.
        """

        if config_services.get_active('environment', 'debug', default=False) is True:
            raise JSONBodyDecodingError('Failed to decode JSON '
                                        'object: [{error}]'.format(error=error))

        self._on_bad_request_received(JSONBodyDecodingError)

    def on_body_loading_failed(self, error):
        """
        raises an error on body loading failure.

        :param Exception error: exception that occurred on loading the body.

        :raises BodyDecodingError: body decoding error.
        """

        if config_services.get_active('environment', 'debug', default=False) is True:
            raise BodyDecodingError('Failed to decode request '
                                    'body: [{error}]'.format(error=error))

        self._on_bad_request_received(BodyDecodingError)

    def _on_bad_request_received(self, error_class):
        """
        raises a generic error on receiving a bad request.

        :param type[BadRequestError] error_class: error class type that has been occurred.

        :raises BadRequestError: bad request error.
        """

        raise error_class(_('The browser (or proxy) sent a request '
                            'that this server could not understand.'))

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

        if isinstance(user, dict):
            self._cacheable_user = CacheableDict(user)
        else:
            self._cacheable_user = user

    def cacheable_user(self):
        """
        gets the cacheable object of current user.

        if the user object is not a dict, it returns the same object.
        otherwise returns a `CacheableDict` object of user dict.

        :rtype: object | CacheableDict
        """

        return self._cacheable_user

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
    def locale(self):
        """
        gets the locale of current request.

        returns None if locale is not set.

        :rtype: str
        """

        return self.get_context(self.LOCALE_CONTEXT_KEY, None)

    @property
    def timezone(self):
        """
        gets the timezone of current request.

        returns None if timezone is not set.

        :rtype: str
        """

        return self.get_context(self.TIMEZONE_CONTEXT_KEY, None)

    @property
    def authorization(self):
        """
        gets the authorization header of current request.

        returns None if authorization header is not set.

        :rtype: str
        """

        return self.get_context(self.AUTHORIZATION_CONTEXT_KEY, None)
