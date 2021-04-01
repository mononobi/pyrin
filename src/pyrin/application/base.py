# -*- coding: utf-8 -*-
"""
application base module.
"""

import os

from collections import OrderedDict

from time import time

import dotenv

from flask.app import setupmethod
from flask.ctx import has_request_context
from flask import Flask, request as flask_request, _request_ctx_stack as request_stack

import pyrin
import pyrin.converters.serializer.services as serializer_services
import pyrin.packaging.services as packaging_services
import pyrin.configuration.services as config_services
import pyrin.security.authentication.services as authentication_services
import pyrin.security.session.services as session_services
import pyrin.logging.services as logging_services
import pyrin.processor.mimetype.services as mimetype_services
import pyrin.processor.response.services as response_services
import pyrin.utils.misc as misc_utils
import pyrin.utils.path as path_utils
import pyrin.utils.function as function_utils

from pyrin.api.router.structs import CoreURLMap
from pyrin.application.container import _set_app
from pyrin.api.router.handlers.protected import ProtectedRoute
from pyrin.application.enumerations import ApplicationStatusEnum
from pyrin.application.hooks import ApplicationHookBase, PackagingHook
from pyrin.application.mixin import SignalMixin
from pyrin.converters.json.decoder import CoreJSONDecoder
from pyrin.converters.json.encoder import CoreJSONEncoder
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.core.structs import DTO, Manager, CoreHeaders
from pyrin.core.mixin import HookMixin
from pyrin.database.transaction.contexts import atomic_context
from pyrin.packaging import PackagingPackage
from pyrin.packaging.component import PackagingComponent
from pyrin.settings.static import DEFAULT_COMPONENT_KEY
from pyrin.utils.custom_print import print_warning
from pyrin.utils.dictionary import make_key_upper
from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.processor.response.wrappers.base import CoreResponse
from pyrin.processor.request.wrappers.base import CoreRequest
from pyrin.application.structs import ApplicationContext, ApplicationComponent, \
    ApplicationSingletonMeta, Component
from pyrin.application.exceptions import DuplicateContextKeyError, InvalidComponentTypeError, \
    InvalidComponentIDError, DuplicateComponentIDError, DuplicateRouteURLError, \
    InvalidRouteFactoryTypeError, InvalidApplicationStatusError, \
    ApplicationInScriptingModeError, ComponentAttributeError, \
    ApplicationIsNotSubclassedError, InvalidApplicationHookTypeError, \
    OverwritingEndpointIsNotAllowedError, InvalidStaticHostAndHostMatchingError


class Application(Flask, HookMixin, SignalMixin,
                  metaclass=ApplicationSingletonMeta):
    """
    application class.

    server must initialize an instance of a subclass of this class at startup.
    """

    # the application looks for these stores to configure itself.
    # they should be present in settings folder of the upper
    # level application.
    CONFIG_STORES = ['application',
                     'communication',
                     'environment']

    # pyrin default settings path will be registered in application context with this key.
    PYRIN_DEFAULT_SETTINGS_CONTEXT_KEY = 'default_settings_path'

    # settings path will be registered in application context with this key.
    SETTINGS_CONTEXT_KEY = 'settings_path'

    # migrations path will be registered in application context with this key.
    MIGRATIONS_CONTEXT_KEY = 'migrations_path'

    # locale path will be registered in application context with this key.
    LOCALE_CONTEXT_KEY = 'locale_path'

    # pyrin main package path will be registered in application context with this key.
    PYRIN_PATH_CONTEXT_KEY = 'pyrin_path'

    # application main package path will be registered in application context with this key.
    APPLICATION_PATH_CONTEXT_KEY = 'application_path'

    # pyrin root path will be registered in application context with this key.
    # pyrin root path is where pyrin main package is located.
    ROOT_PYRIN_PATH_CONTEXT_KEY = 'root_pyrin_path'

    # application root path will be registered in application context with this key.
    # root path is where application main package and other files are located.
    ROOT_APPLICATION_PATH_CONTEXT_KEY = 'root_application_path'

    # default packaging component to be used by application.
    # if you want to change the default one, you could subclass
    # Application and set `packaging_component_class` to your desired one.
    # this design is compatible with other flask subclassing features.
    # note that your custom packaging component class should not use `@component`
    # decorator to register itself, application will register it instead.
    packaging_component_class = PackagingComponent

    # a function to be used as default response converter when
    # the mimetype of response could not be detected from its body or
    # the founded mimetype could not be handled by pyrin itself.
    # this function should accept a single parameter as response body
    # and extra optional keyword arguments. the founded mimetype will be
    # passed to this function as 'mimetype' keyword argument. metadata for
    # pagination is also passed to this function using 'metadata' keyword.
    # paginator instance will also passed to this function using 'paginator'
    # keyword. the function must return a response object or an object which
    # could be converted to response by flask.
    default_response_converter = None

    headers_class = CoreHeaders
    url_rule_class = ProtectedRoute
    url_map_class = CoreURLMap
    response_class = CoreResponse
    request_class = CoreRequest
    json_decoder = CoreJSONDecoder
    json_encoder = CoreJSONEncoder
    hook_type = ApplicationHookBase
    invalid_hook_type_error = InvalidApplicationHookTypeError

    def __init__(self, **options):
        """
        initializes an instance of Application.

        :keyword str import_name: the name of the application package.
                                  it will be assumed equal to first part
                                  of application package name if not provided.
                                  for example: `pyrin`.
                                  but if the main package name of application includes
                                  more that one package you should provide it manually.
                                  for example: `tests.unit`.

        :keyword str static_url_path: can be used to specify a different path for the
                                      static files on the web. defaults to the name
                                      of the `static_folder` directory.

        :keyword str static_folder: the folder with static files that is served at
                                    `static_url_path`. relative to the application
                                    `root_path` or an absolute path. defaults to `static'.

        :keyword str static_host: the host to use when adding the static route.
                                  defaults to None. required when using `host_matching=True`
                                  with a `static_folder` configured.

        :keyword bool host_matching: set `url_map.host_matching` attribute.
                                     defaults to False.

        :keyword str subdomain_matching: consider the subdomain relative to
                                         `SERVER_NAME` when matching routes.
                                         defaults to False.

        :keyword str template_folder: the folder that contains the templates that should
                                      be used by the application. defaults to
                                      `templates` folder in the root path of the application.

        :keyword str instance_path: an alternative instance path for the application.
                                    by default the folder `instance` next to the
                                    package or module is assumed to be the instance path.

        :keyword bool instance_relative_config: if set to `True` relative filenames
                                                for loading the config are assumed to
                                                be relative to the instance path instead
                                                of the application root.

        :keyword str root_path: flask by default will automatically calculate the path
                                to the root of the application. in certain situations
                                this cannot be achieved (for instance if the package
                                is a python 3 namespace package) and needs to be
                                manually defined.

        :keyword bool scripting_mode: specifies that the application has been started in
                                      scripting mode. application will not be run in
                                      scripting mode and some application hooks will not
                                      get fired when the application has initialized in
                                      scripting mode. defaults to False, if not provided.

        :keyword bool force_json_response: specifies that if response object is
                                           not an html string, consider it as json
                                           and convert it to be json serializable.
                                           even if it is not a dict.
                                           defaults to True if not provided.

        :keyword str settings_directory: settings directory name.
                                         if not provided, defaults to `settings`.

        :keyword str migrations_directory: migrations directory name.
                                           if not provided, defaults to `migrations`.

        :keyword str locale_directory: locale directory name.
                                       if not provided, defaults to `locale`.

        :raises ApplicationIsNotSubclassedError: application is not subclassed error.
        """

        self._assert_is_subclassed()

        self.__status = ApplicationStatusEnum.INITIALIZING
        self._scripting_mode = options.get('scripting_mode', False)
        self._force_json_response = options.get('force_json_response', True)
        self._version = 'Not Provided'

        self._import_name = options.get('import_name', None)
        if self._import_name is not None and (self._import_name == '' or
                                              self._import_name.isspace()):
            self._import_name = None

        flask_kw = self._remove_flask_unrecognized_keywords(**options)
        # we should pass `static_folder=None` to prevent flask from
        # adding static route on startup, then we register it after application is loaded.
        flask_kw.update(static_folder=None)
        super().__init__(self.get_application_name(), **flask_kw)

        # Flask does not call 'super()' in its '__init__()' method.
        # so we have to start initialization of other parents manually.
        HookMixin.__init__(self, **options)

        self._context = ApplicationContext()
        self._components = ApplicationComponent()

        # we have to register some components manually because they are
        # referenced in `application.base` module and could not be loaded
        # automatically because packaging package could not handle them.
        self._register_required_components()

        # setting the application instance in application container module.
        _set_app(self)

        self._register_required_hooks()

        # we should load application at this stage to be able to perform pytest
        # tests after application has been fully loaded. because if we call
        # application.run(), we could not continue execution of other codes.
        self._load(**options)

        self.static_folder = options.get('static_folder', 'static')
        self._register_static_route(options.get('static_host'), self.url_map.host_matching)

    @setupmethod
    def _register_static_route(self, static_host, host_matching, **options):
        """
        registers static route if required.

        :param str static_host: the host to use when adding the static route.
                                defaults to None. required when using `host_matching=True`
                                with a `static_folder` configured.

        :param bool host_matching: set `url_map.host_matching` attribute.
                                   defaults to False.

        :raises InvalidStaticHostAndHostMatchingError: invalid static host and
                                                       host matching error.
        """

        if self.has_static_folder:
            if bool(static_host) != host_matching:
                raise InvalidStaticHostAndHostMatchingError('Invalid static_host/'
                                                            'host_matching combination.')

            self.add_url_rule(self.static_url_path + '/<path:filename>',
                              view_func=self.send_static_file,
                              authenticated=False,
                              endpoint='static',
                              host=static_host)

    def _remove_flask_unrecognized_keywords(self, **options):
        """
        removes any keyword argument which is not recognized by `Flask.__init__()` method.

        it returns a new dict with all recognized keyword arguments.

        :rtype: dict
        """

        result = dict(**options)
        result.pop('import_name', None)
        result.pop('scripting_mode', None)
        result.pop('settings_directory', None)
        result.pop('migrations_directory', None)
        result.pop('locale_directory', None)
        result.pop('force_json_response', None)

        return result

    def _assert_is_subclassed(self):
        """
        asserts that current application instance is subclassed from `Application`.

        and is not a direct instance of `Application` itself.

        :raises ApplicationIsNotSubclassedError: application is not subclassed error.
        """

        if type(self) is Application:
            raise ApplicationIsNotSubclassedError('Current application instance is a direct '
                                                  'instance of [{base}]. you must subclass '
                                                  'from [{base}] in your project and create '
                                                  'an instance of that class to run your '
                                                  'application. this is needed for pyrin to be '
                                                  'able to resolve different paths correctly.'
                                                  .format(base=self))

    def is_scripting_mode(self):
        """
        gets a value indicating that application has been started in scripting mode.

        some application hooks will not fire in this mode. like 'before_application_run'.
        """

        return self._scripting_mode

    @setupmethod
    def _register_required_components(self):
        """
        registers required components that the Application needs
        to reference to them immediately.

        this type of components could not be registered using @component decorator,
        because they will be referenced before Application instance gets initialized.

        note that implementation-wise, application package should depend on other
        packages services as few as possible, so be careful if you needed some external
        packages services inside application package, probably it would be better to
        change your design that enforces the application to use other packages services.
        """

        self.register_component(self.packaging_component_class(
            PackagingPackage.COMPONENT_NAME))

    @setupmethod
    def _register_required_hooks(self):
        """
        registers the required hooks that the Application needs them.

        this type of hooks could not be registered using @hook decorators,
        because they will be referenced before Application instance gets
        initialized.
        """

        packaging_services.register_hook(PackagingHook())

    def _set_status(self, status):
        """
        sets the application status.

        status must be from ApplicationStatusEnum.

        :param str status: application status.

        :enum status:
            INITIALIZING = 'Initializing'
            LOADING = 'Loading'
            READY = 'Ready'
            RUNNING = 'Running'
            TERMINATED = 'Terminated'

        raises InvalidApplicationStatusError: invalid application status error.
        """

        if status not in ApplicationStatusEnum:
            raise InvalidApplicationStatusError('Application status [{state}] is not valid.'
                                                .format(state=status))

        old_status = self.__status
        self.__status = status

        if old_status != status:
            self._application_status_changed(old_status, status)

    def get_status(self):
        """
        gets the application status.

        :rtype: str
        """

        return self.__status

    def add_context(self, key, value, **options):
        """
        adds the given key and it's value into the application context.

        :param str key: related key for storing application context.
        :param object value: related value for storing in application context.

        :keyword bool replace: specifies that if there is already a value with
                               the same key in application context, it should be updated
                               with new value, otherwise raise an error. defaults to False.

        :raises DuplicateContextKeyError: duplicate context key error.
        """

        replace = options.get('replace', False)
        if replace is not True and key in self._context:
            raise DuplicateContextKeyError('Key [{key}] is already available in application '
                                           'context and "replace=True" option is not set, so '
                                           'the new value could not be added.'
                                           .format(key=key))

        self._context[key] = value

    def get_context(self, key, **options):
        """
        gets the application context value that belongs to given key.

        :param str key: key for requested application context.

        :keyword object default: default value to be returned if key is not available.
                                 otherwise, it raises an error if key is not available.

        :raises ContextAttributeError: context attribute error.

        :returns: related value to given key.
        """

        if 'default' not in options:
            return self._context[key]

        default = options.get('default')
        return self._context.get(key, default)

    @setupmethod
    def register_component(self, component, **options):
        """
        registers given application component or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's id is already available
        in registered components.

        :param Component component: component instance.

        :keyword bool replace: specifies that if there is another registered
                               component with the same id, replace it with the new one.
                               otherwise raise an error. defaults to False.

        :raises InvalidComponentTypeError: invalid component type error.
        :raises InvalidComponentIDError: invalid component id error.
        :raises DuplicateComponentIDError: duplicate component id error.
        """

        if not isinstance(component, Manager):
            raise InvalidComponentTypeError('Input parameter [{component}] is not '
                                            'an instance of [{instance}]. each component '
                                            'class must be subclassed from its respective '
                                            'manager class of the same package and that '
                                            'manager class must be subclassed from [{instance}].'
                                            .format(component=component,
                                                    instance=Manager))

        if not isinstance(component, Component):
            raise InvalidComponentTypeError('Input parameter [{component}] is not '
                                            'an instance of [{instance}].'
                                            .format(component=component,
                                                    instance=Component))

        if not isinstance(component.get_id(), tuple) or \
                len(component.get_id()[0].strip()) == 0:
            raise InvalidComponentIDError('Component [{component}] does '
                                          'not have a valid component id.'
                                          .format(component=component))

        # checking whether is there any registered component with the same id.
        if component.get_id() in self._components.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicateComponentIDError('There is another registered component with '
                                                'id [{id}] but "replace" option is not set, so '
                                                'component [{instance}] could not be registered.'
                                                .format(id=component.get_id(),
                                                        instance=component))

            old_instance = self._components[component.get_id()]

            # we should update all list and dict attributes and also those that their name
            # starts with two consecutive underscores of new component with values
            # from old_instance to prevent loss of any attribute value (for example values
            # that has been added using decorators).
            # this has an obvious caveat, and it is that child classes could not do
            # any customizations on these attributes in their `__init__` method.
            component = self._set_component_attributes(old_instance, component)

            print_warning('Component [{old_instance}] is going to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance, new_instance=component))

        self._components[component.get_id()] = component

    def remove_component(self, component_id):
        """
        removes application component with given id.

        :param tuple[str, object] component_id: component id to be removed.

        :raises ComponentAttributeError: component attribute error.
        """

        if component_id not in self._components:
            raise ComponentAttributeError('Component [{component_id}] is not '
                                          'available in application components.'
                                          .format(component_id=component_id))

        self._components.pop(component_id)

    def _get_safe_current_request(self):
        """
        gets current request in a safe manner.

        meaning that if there is no request in current context,
        returns None instead of raising an error.

        :rtype: CoreRequest
        """

        if has_request_context() is True:
            return flask_request

        return None

    def get_component(self, component_name, **options):
        """
        gets the specified application component.

        :param str component_name: component name.

        :keyword object component_custom_key: component custom key.
                                              if not provided, tries to get it from
                                              request object, if not found,
                                              `DEFAULT_COMPONENT_KEY` will be used.

        :raises InvalidComponentNameError: invalid component name error.
        :raises ComponentAttributeError: component attribute error.

        :rtype: Component
        """

        component_custom_key = options.get('component_custom_key', None)

        if component_custom_key is None:
            component_custom_key = self._extract_component_custom_key()

        # checking whether is there any custom implementation.
        component_custom_id = \
            Component.make_component_id(component_name,
                                        component_custom_key=component_custom_key)

        if component_custom_id in self._components.keys():
            return self._components[component_custom_id]

        # getting default component.
        component_default_id = Component.make_component_id(component_name)
        return self._components[component_default_id]

    def _extract_component_custom_key(self):
        """
        gets `component_custom_key` from current request.

        note that if application is in any state lower than `READY`,
        it always returns the default component key.

        :rtype: object
        """

        # before application reaches the `READY` state,
        # we should always use the default component key.
        if self.get_status() in (ApplicationStatusEnum.INITIALIZING,
                                 ApplicationStatusEnum.LOADING):

            return DEFAULT_COMPONENT_KEY

        # this method is the only place that we should access request
        # directly and not from session services, because of circular calling problem.
        client_request = self._get_safe_current_request()
        if client_request is not None:
            return client_request.component_custom_key

        return DEFAULT_COMPONENT_KEY

    def _load(self, **options):
        """
        loads application configs and components.
        """

        self._set_status(ApplicationStatusEnum.LOADING)
        self._resolve_required_paths(**options)
        self._load_environment_variables()
        packaging_services.load_components(**options)
        self._load_version()

        # calling `after_application_loaded` method of all registered hooks.
        self._after_application_loaded()

        # calling `application_initialized` method of all registered hooks.
        self._application_initialized()
        self._set_status(ApplicationStatusEnum.READY)

        if self.is_scripting_mode() is False:
            self._prepare_runtime_data()

    def _resolve_required_paths(self, **options):
        """
        resolves all required paths for application.
        """

        self._resolve_settings_path(**options)
        self._resolve_migrations_path(**options)
        self._resolve_locale_path(**options)

    def _load_version(self):
        """
        loads application version.

        it looks for a `__version__` attribute in main package of application.
        this method could be overridden in subclasses to change behavior.
        """

        package_name = path_utils.get_main_package_name(self.__module__)
        package = packaging_services.load(package_name)
        version = getattr(package, '__version__', None)

        if version is not None:
            self._version = version

    def _load_configs(self, **options):
        """
        loads all configurations related to application package.
        """

        config_services.load_configurations(*self.CONFIG_STORES, **options)
        for store_name in self.CONFIG_STORES:
            config_dict = config_services.get_all(store_name, **options)
            self.configure(config_dict)

    @setupmethod
    def load_configs(self, **options):
        """
        loads all configurations related to application package.

        normally, you should not call this method manually.
        """

        self._load_configs(**options)

    def _configure(self, config_store):
        """
        configures the application with given dict.

        all keys will be converted to uppercase for flask compatibility.

        :param dict config_store: a dictionary containing configuration key/values.
        """

        upper_dict = make_key_upper(config_store)
        self.config.update(upper_dict)

    @setupmethod
    def configure(self, config_store):
        """
        configures the application with given dict.

        all keys will be converted to uppercase for flask compatibility.

        :param dict config_store: a dictionary containing configuration key/values.
        """

        self._configure(config_store)

    def run(self, host=None, port=None, debug=None,
            load_dotenv=True, **options):
        """
        runs the Application instance.

        :param str host: the hostname to listen on. set this to `0.0.0.0` to
                         have the server available externally as well. defaults
                         to `127.0.0.1` or the host in the `SERVER_NAME` config
                         variable if present.

        :param int port: the port of the webserver. defaults to `5000` or the
                         port defined in the `SERVER_NAME` config variable if present.

        :param bool debug: if given, enable or disable debug mode.

        :param bool load_dotenv: load the nearest `.env` and `.flaskenv`
                                 files to set environment variables. will also
                                 change the working directory to the directory
                                 containing the first file found.

        :keyword bool use_reloader: specifies that the server should automatically
                                    restart the python process if modules were changed.

        :keyword bool use_debugger: specifies that the werkzeug debugging
                                    system should be used.

        :keyword bool threaded: specifies that the process should handle
                                each request in a separate thread.

        :raises ApplicationInScriptingModeError: application in scripting mode error.
        """

        if self.is_scripting_mode() is True:
            raise ApplicationInScriptingModeError('Application has been initialized in '
                                                  'scripting mode, so it could not be run.')

        self._before_application_run()
        self._set_status(ApplicationStatusEnum.RUNNING)
        host, port = self._get_communication_configs(host, port)
        super().run(host, port, debug, load_dotenv, **options)

    def _get_communication_configs(self, host, port):
        """
        gets the host and port to use for application.

        :param str host: host name or ip address.
        :param int port: port number.

        :returns: tuple[str host, int port]
        :rtype: tuple[str, int]
        """

        if host in (None, ''):
            host = config_services.get_active('communication', 'server_host')

        if port is None:
            port = config_services.get_active('communication', 'server_port')

        return host, port

    def dispatch_request(self):
        """
        does the request dispatching.

        matches the URL and returns the return value of the view or
        error handlers. this does not have to be a response object.
        in order to convert the return value to a proper response object,
        call `make_response` function.

        :raises AuthenticationFailedError: authentication failed error.
        :raises ViewFunctionRequiredParamsError: view function required params error.
        """

        # we have to override whole `dispatch_request` method to be able to
        # customize it, because of the flask design that everything is embedded
        # inside the `dispatch_request` method.

        client_request = session_services.get_current_request()
        if client_request.routing_exception is not None:
            self.raise_routing_exception(client_request)

        route = client_request.url_rule

        # if we provide automatic options for this URL and the
        # request came with the OPTIONS method, reply automatically.
        if getattr(route, 'provide_automatic_options', False) \
           and client_request.method == HTTPMethodEnum.OPTIONS:
            return self.make_default_options_response()

        # otherwise call the handler for this route.
        return route.handle(client_request.get_inputs())

    def _authenticate(self, client_request):
        """
        authenticates given request.

        :param CoreRequest client_request: request to be authenticated.

        :raises AuthenticationFailedError: authentication failed error.
        """

        authentication_services.authenticate(client_request)

    def get_current_url_adapter(self):
        """
        gets url adapter of current request.

        if request context is not present, this method raises an error.

        :rtype: MapAdapter
        """

        return request_stack.top.url_adapter

    def make_response(self, rv):
        """
        converts the return value from a view function to an instance of `CoreResponse`.

        note that the `rv` value before passing to base method must
        be a `tuple`, `dict`, `str` or `CoreResponse`. otherwise
        it causes an error.

        :param tuple | dict | str | CoreResponse rv: the return value
                                                     from the view function.

        :rtype: CoreResponse
        """

        body, status_code, headers = response_services.unpack_response(rv)
        if not isinstance(body, self.response_class) and not callable(body):
            mimetype = mimetype_services.get_mimetype(body)
            if mimetype != MIMETypeEnum.HTML and (mimetype != MIMETypeEnum.JSON or
                                                  not isinstance(body, str)):
                body, metadata, paginator = self._paginate_result(body)
                if self._force_json_response is True:
                    body = self._prepare_json(body, metadata=metadata, paginator=paginator)
                elif self.default_response_converter is not None:
                    body = self.default_response_converter(body,
                                                           metadata=metadata,
                                                           mimetype=mimetype,
                                                           paginator=paginator)

                if body is None:
                    body = ''

        response = response_services.pack_response(body, status_code, headers)
        result = super().make_response(response)
        result.original_data = body
        return result

    def _paginate_result(self, body, **options):
        """
        paginates response body if required.

        it returns the paginated result and pagination metadata and also the paginator itself.
        if pagination is not done, it returns the same input and None as metadata and paginator.

        :param tuple | dict | str body: the return value from the view function.

        :returns: tuple[list | tuple | dict | str  items, dict metadata, PaginatorBase paginator]
        :rtype: tuple[list | tuple | dict | str, dict, PaginatorBase]
        """

        paginator = session_services.get_request_context('paginator', None)
        if paginator is not None and isinstance(body, list):
            body, metadata = paginator.paginate(body)
            return body, metadata, paginator

        return body, None, None

    def _prepare_json(self, rv, metadata=None, paginator=None):
        """
        prepares the input value to be convertible to json.

        :param object rv: the return value from the view function.

        :param dict metadata: metadata that should be injected into
                              response for pagination.

        :param PaginatorBase paginator: paginator that has been used.

        :rtype: dict
        """

        if rv is None:
            rv = DTO()
        else:
            rv = self._serialize_result(rv, paginator)

        # we could not return a list as response, so we wrap
        # the result in a dict when we want to return a list.
        if isinstance(rv, list):
            result = OrderedDict()
            if metadata is not None:
                result.update(metadata)
            else:
                result.update(count=len(rv))
            result.update(results=rv)
            rv = result

        # we should wrap all single values into a
        # dict before returning it to client.
        if not isinstance(rv, (tuple, dict, self.response_class)):
            rv = DTO(value=rv)

        return rv

    def _serialize_result(self, rv, paginator=None):
        """
        serializes the return value if needed.

        this method could be overridden in subclasses.
        it must return a dict or a list of dicts on success or
        the same exact input if could not convert it.

        :param object rv: the return value from the view function.
        :param PaginatorBase paginator: paginator that has been used.

        :rtype: dict | list[dict]
        """

        result_schema = session_services.get_request_context('result_schema', None)
        if result_schema is not None:
            return result_schema.filter(rv, paginator=paginator)

        return serializer_services.serialize(rv)

    @setupmethod
    def add_url_rule(self, rule, view_func,
                     provide_automatic_options=None, **options):
        """
        connects a url rule. the provided view_func will be registered with the endpoint.

        if there is another rule with the same url and http methods and `replace=True`
        option is provided, it will be replaced. otherwise an error will be raised.

        a note about endpoint. pyrin will handle endpoint generation on its own.
        so there is no endpoint parameter in this method's signature.
        this is required to be able to handle uniqueness of endpoints and managing them.
        despite flask, pyrin will not require you to define view functions with unique names.
        you could define view functions with the same name in different modules. but to
        ensure the uniqueness of endpoints, pyrin will use the fully qualified name
        of function as endpoint. for example: `pyrin.api.services.create_route`.
        so you could figure out endpoint for any view function to use it in places
        like `url_for` method.

        pyrin handles endpoints this way to achieve these two important features:

        1. dismissal of the need for view function name uniqueness.
           when application grows, it's nonsense to be forced to have
           unique view function names at application level.

        2. managing routes with the same url and http methods, and informing
           the developer about them to prevent accidental replacements. and also
           providing a way to replace a route by another route with the same url
           and http methods if that is what developer actually wants.
           when application grows, it becomes a point of failure when you have no
           idea that you've registered a similar route in multiple places and only
           one of them will be get called based on registration order.

        :param str rule: the url rule as string.

        :param function view_func: the function to call when serving a request to the
                                   provided endpoint.

        :param bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                               added automatically.
                                               this can also be controlled by setting the
                                               `view_func.provide_automatic_options = False`
                                               before adding the rule.

        :keyword str | tuple[str] methods: http methods that this rule should handle.
                                           if not provided, defaults to `GET`.

        :keyword PermissionBase | tuple[PermissionBase] permissions: all required permissions
                                                                     for accessing this route.

        :keyword bool authenticated: specifies that this route could not be accessed
                                     if the requester has not been authenticated.
                                     defaults to True if not provided.

        :keyword bool fresh_auth: specifies that this route could not be accessed
                                  if the requester has not a fresh authentication.
                                  fresh authentication means an authentication that
                                  has been done by providing user credentials to
                                  server. defaults to False if not provided.

        :keyword bool replace: specifies that this route must replace any existing
                               route with the same url and http methods or raise
                               an error if not provided. defaults to False.

        :keyword dict defaults: an optional dict with defaults for other rules with the
                                same endpoint. this is a bit tricky but useful if you
                                want to have unique urls.

        :keyword str subdomain: the subdomain rule string for this rule. If not specified the
                                rule only matches for the `default_subdomain` of the map. if
                                the map is not bound to a subdomain this feature is disabled.

        :keyword bool strict_slashes: override the `Map` setting for `strict_slashes` only for
                                      this rule. if not specified the `Map` setting is used.

        :keyword bool merge_slashes: override `Map.merge_slashes` for this rule.

        :keyword bool build_only: set this to True and the rule will never match but will
                                  create a url that can be build. this is useful if you have
                                  resources on a subdomain or folder that are not handled by
                                  the WSGI application (like static data)

        :keyword str | callable redirect_to: if given this must be either a string
                                             or callable. in case of a callable it's
                                             called with the url adapter that
                                             triggered the match and the values
                                             of the url as keyword arguments and has
                                             to return the target for the redirect,
                                             otherwise it has to be a string with
                                             placeholders in rule syntax.

        :keyword bool alias: if enabled this rule serves as an alias for another rule with
                             the same endpoint and arguments.

        :keyword str host: if provided and the url map has host matching enabled this can be
                           used to provide a match rule for the whole host. this also means
                           that the subdomain feature is disabled.

        :keyword bool websocket: if set to True, this rule is only matches for
                                 websocket (`ws://`, `wss://`) requests. by default,
                                 rules will only match for http requests.
                                 defaults to False if not provided.

        :keyword int max_content_length: max content length that this route could handle,
                                         in bytes. if not provided, it will be set to
                                         `restricted_max_content_length` api config key.
                                         note that this value should be lesser than or equal
                                         to `max_content_length` api config key, otherwise
                                         it will cause an error.

        :keyword int status_code: status code to be returned on successful responses.
                                  defaults to corresponding status code of request's
                                  http method if not provided.

        :note status_code: it could be a value from `InformationResponseCodeEnum`
                           or `SuccessfulResponseCodeEnum` or `RedirectionResponseCodeEnum`.

        :keyword bool strict_status: specifies that it should only consider
                                     the status code as processed if it is from
                                     `InformationResponseCodeEnum` or
                                     `SuccessfulResponseCodeEnum` or
                                     `RedirectionResponseCodeEnum` values. otherwise
                                     all codes from `INFORMATION_CODE_MIN`
                                     to `INFORMATION_CODE_MAX` or from
                                     `SUCCESS_CODE_MIN` to `SUCCESS_CODE_MAX`
                                     or from `REDIRECTION_CODE_MIN` to
                                     `REDIRECTION_CODE_MAX` will be considered
                                     as processed. defaults to True if not provided.

        :keyword str | list[str] environments: a list of all environments that this
                                               route must be exposed on them.
                                               the values could be from all available
                                               environments in environments config store.
                                               for example: `production`, `development`.
                                               if not provided, the route will be exposed
                                               on all environments.

        :keyword ResultSchema | type[ResultSchema] result_schema: result schema to be used
                                                                  to filter results. it could
                                                                  be an instance or a type
                                                                  of `ResultSchema` class.

        :keyword bool indexed: specifies that list results must
                               include an extra field as row index.
                               the name of the index field and the initial value
                               of index could be provided by `index_name` and
                               `start_index` respectively. `indexed` keyword has
                               only effect if the returning result contains a list
                               of objects.

        :keyword str index_name: name of the extra field to contain
                                 the row index of each result. if not provided
                                 defaults to `row_num` value.

        :keyword int start_index: the initial value of row index. if not
                                  provided, starts from 1.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
                                                      starts with underscore `_`, should not
                                                      be included in result dict. defaults to
                                                      `SECURE_TRUE` if not provided. it will
                                                      be used only for entity conversion.
                                                      this value will override the
                                                      corresponding value of `result_schema`
                                                      if provided.

        :keyword int depth: a value indicating the depth for conversion.
                            for example if entity A has a relationship with
                            entity B and there is a list of B in A, if `depth=0`
                            is provided, then just columns of A will be available
                            in result dict, but if `depth=1` is provided, then all
                            B entities in A will also be included in the result dict.
                            actually, `depth` specifies that relationships in an
                            entity should be followed by how much depth.
                            note that, if `columns` is also provided, it is required to
                            specify relationship property names in provided columns.
                            otherwise they won't be included even if `depth` is provided.
                            defaults to `default_depth` value of database config store.
                            please be careful on increasing `depth`, it could fail
                            application if set to higher values. choose it wisely.
                            normally the maximum acceptable `depth` would be 2 or 3.
                            there is a hard limit for max valid `depth` which is set
                            in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                            `depth` value than this limit, will cause an error.
                            it will be used only for entity conversion.
                            this value will override the corresponding value of
                            `result_schema` if provided.

        :keyword bool no_cache: a value indicating that the response returning from this route
                                must have a `Cache-Control: no-cache` header. this header will
                                be automatically added. defaults to False if not provided.

        :keyword int request_limit: number of allowed requests to this
                                    route before it unregisters itself.
                                    defaults to None if not Provided.

        :keyword int lifetime: number of seconds in which this route must remain
                               responsive after initial registration. after this
                               period, the route will unregister itself.
                               defaults to None if not provided.

        :note request_limit, lifetime: if both of these values are provided, this
                                       route will unregister itself if any of
                                       these two conditions are met.

        :keyword bool paged: specifies that this route should return paginated results.
                             defaults to False if not provided.

        :keyword int page_size: default page size for this route.
                                defaults to `default_page_size` from
                                `database` config store if not provided.

        :keyword int max_page_size: maximum page size that client is allowed
                                    to request for this route. defaults to
                                    `max_page_size` from `database` configs store
                                    if not provided.

        :keyword bool cors_enabled: specifies that cross origin resource sharing is enabled.
                                    if not provided, it will be get from cors config store.

        :keyword bool cors_always_send: specifies that cors headers must be included in
                                        response even if the request does not have origin header.
                                        if not provided, it will be get from cors config store.

        :keyword list[str] cors_allowed_origins: a list of extra allowed origins to be used
                                                 in conjunction with default allowed ones.

        :keyword list[str] cors_exposed_headers: extra exposed headers to be combined
                                                 with default ones.

        :keyword list[str] cors_allowed_headers: extra allowed headers to be combined
                                                 with default ones.

        :keyword bool cors_allow_credentials: specifies that browsers are allowed to pass
                                              response headers to front-end javascript code
                                              if the route is authenticated.
                                              if not provided, it will be get from cors config
                                              store.

        :keyword int cors_max_age: maximum number of seconds to cache results.
                                   if not provided, it will be get from cors config store.

        :raises DuplicateRouteURLError: duplicate route url error.
        :raises OverwritingEndpointIsNotAllowedError: overwriting endpoint is not allowed error.
        :raises PageSizeLimitError: page size limit error.
        :raises MaxContentLengthLimitMismatchError: max content length limit mismatch error.
        :raises InvalidViewFunctionTypeError: invalid view function type error.
        :raises InvalidResultSchemaTypeError: invalid result schema type error.
        :raises InvalidResponseStatusCodeError: invalid response status code error.
        """

        environments = options.get('environments')
        if self._should_expose_route(rule, view_func,
                                     environments) is not True:
            return

        endpoint = options.get('endpoint')
        if endpoint in (None, ''):
            endpoint = self.generate_endpoint(view_func, **options)
            options.update(endpoint=endpoint)

        methods = options.pop('methods', None)
        if methods is not None:
            methods = misc_utils.make_iterable(methods, tuple)

        # if the methods are not given and the view_func object knows its
        # methods we can use that instead. if neither exists, we go with
        # a tuple of only `GET` as default.
        if methods is None:
            methods = getattr(view_func, 'methods', None) or (HTTPMethodEnum.GET,)

        methods = set(item.upper() for item in methods)
        required_methods = set(getattr(view_func, 'required_methods', ()))

        # starting with flask 0.8 the view_func object can disable and
        # force-enable the automatic options handling.
        if provide_automatic_options is None:
            provide_automatic_options = getattr(
                view_func, 'provide_automatic_options', None)

        if provide_automatic_options is None:
            if HTTPMethodEnum.OPTIONS not in methods:
                provide_automatic_options = True
                required_methods.add(HTTPMethodEnum.OPTIONS)
            else:
                provide_automatic_options = False

        # add the required methods now.
        methods |= required_methods

        # we have to put `view_function=view_func` into options to be able to deliver it
        # to route initialization in the super method. that's because of flask design
        # that does not forward all params to inner method calls.
        options.update(view_function=view_func)

        route = self.url_rule_class(rule, methods=methods, **options)
        route.provide_automatic_options = provide_automatic_options
        self._add_to_map(route, **options)

        old_func = self.view_functions.get(endpoint)
        if old_func is not None and old_func != view_func:
            old_name = function_utils.get_fully_qualified_name(old_func)
            new_name = function_utils.get_fully_qualified_name(view_func)
            raise OverwritingEndpointIsNotAllowedError('View function [{new_function}] '
                                                       'is overwriting an existing endpoint '
                                                       '[{endpoint}] with registered view '
                                                       'function [{old_function}]. this could '
                                                       'be the result of manually modified '
                                                       'endpoints. pyrin will handle endpoint '
                                                       'generation on its own. so it is '
                                                       'recommended not to define or modify '
                                                       'endpoints manually.'
                                                       .format(new_function=new_name,
                                                               endpoint=endpoint,
                                                               old_function=old_name))

        self.view_functions[endpoint] = view_func

    def _should_expose_route(self, url, view_func, environments):
        """
        gets a value indicating that given route must be exposed on current environment.

        :param str url: the url rule as string.

        :param function view_func: the function to call when serving a request to the
                                   provided endpoint.

        :param str | list[str] environments: a list of all environments that this
                                             route must be exposed on them.
                                             the values could be from all available
                                             environments in environments config store.
                                             for example: `production`, `development`.
                                             if not provided, the route will be exposed
                                             on all environments.

        :rtype: bool
        """

        environments = misc_utils.make_iterable(environments, list)
        should_expose = True
        if len(environments) > 0:
            current_env = config_services.get_active_section_name('environment')
            should_expose = current_env in environments
            if should_expose is not True:
                func_name = function_utils.get_fully_qualified_name(view_func)
                print_warning('Route [{url}] on view function [{func}] will only be '
                              'exposed on {env} environments. the current environment '
                              'is [{current}].'.format(url=url, func=func_name,
                                                       env=environments, current=current_env))
        return should_expose

    def generate_endpoint(self, func, **options):
        """
        generates endpoint for given function.

        pyrin will assume endpoint as function's fully qualified name.
        this method could be overridden in subclasses to change the endpoint generation.

        :param function func: function to generate endpoint for it.

        :rtype: str
        """

        return function_utils.get_fully_qualified_name(func)

    def _add_to_map(self, route, **options):
        """
        adds the given route into map.

        :param RouteBase route: route instance to be added into map.

        :keyword bool replace: specifies that this route must replace
                               any existing route with the same url and http
                               methods or raise an error if not provided.
                               defaults to False.

        :raises DuplicateRouteURLError: duplicate route url error.
        """

        replace = options.get('replace', False)
        existing_routes = self.url_map.get_routes_by_url(route.rule)

        duplicate_methods = DTO()
        for item in existing_routes:
            duplicated = item.get_duplicate_methods(route.methods)
            if len(duplicated) > 0:
                duplicated_for_show = list(duplicated)
                old_func = function_utils.get_fully_qualified_name(item.view_function)
                new_func = function_utils.get_fully_qualified_name(route.view_function)
                if replace is True:
                    duplicate_methods[tuple(duplicated)] = item
                    print_warning('Registered route with url [{url}] for http methods '
                                  '{methods} on view function [{old_func}] is going to be '
                                  'replaced by a new route on view function [{new_func}].'
                                  .format(url=route.rule, methods=duplicated_for_show,
                                          old_func=old_func, new_func=new_func))
                else:
                    raise DuplicateRouteURLError('There is another registered route with the '
                                                 'same url [{url}] and http methods {methods} '
                                                 'on view function [{old_func}], but "replace" '
                                                 'option is not set, so the new route on view '
                                                 'function [{new_func}] could not be registered.'
                                                 .format(url=route.rule,
                                                         methods=duplicated_for_show,
                                                         old_func=old_func, new_func=new_func))

        if len(duplicate_methods) > 0:
            for methods, duplicate_route in duplicate_methods.items():
                duplicate_route.remove_methods(methods)
                if not duplicate_route.is_operational:
                    self.url_map.remove(duplicate_route)

        self.url_map.add(route)

    @setupmethod
    def register_route_factory(self, factory):
        """
        registers a route factory as application url rule class.

        :param callable factory: route factory.
                                 it could be a class or a factory method.

        :raises InvalidRouteFactoryTypeError: invalid route factory type error.
        """

        if not callable(factory):
            raise InvalidRouteFactoryTypeError('Input parameter [{factory}] is not callable.'
                                               .format(factory=factory))

        old_factory = misc_utils.try_get_fully_qualified_name(self.url_rule_class)
        new_factory = misc_utils.try_get_fully_qualified_name(factory)
        print_warning('Registered route factory [{old_factory}] is '
                      'going to be replaced by a new route factory [{new_factory}].'
                      .format(old_factory=old_factory,
                              new_factory=new_factory))

        self.url_rule_class = factory

    def get_current_route_factory(self):
        """
        gets current route factory in use.

        :rtype: callable
        """

        return self.url_rule_class

    def get_default_settings_path(self):
        """
        gets the pyrin default settings path.

        :rtype: str
        """

        result = self.get_context(self.PYRIN_DEFAULT_SETTINGS_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_default_settings_path()
        return self.get_context(self.PYRIN_DEFAULT_SETTINGS_CONTEXT_KEY)

    def get_settings_path(self):
        """
        gets the application settings path.

        :rtype: str
        """

        result = self.get_context(self.SETTINGS_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_settings_path()
        return self.get_context(self.SETTINGS_CONTEXT_KEY)

    def get_migrations_path(self):
        """
        gets the application migrations path.

        :rtype: str
        """

        result = self.get_context(self.MIGRATIONS_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_migrations_path()
        return self.get_context(self.MIGRATIONS_CONTEXT_KEY)

    def get_locale_path(self):
        """
        gets the application locale path.

        :rtype: str
        """

        result = self.get_context(self.LOCALE_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_locale_path()
        return self.get_context(self.LOCALE_CONTEXT_KEY)

    def get_application_main_package_path(self):
        """
        gets the application main package path.

        :rtype: str
        """

        result = self.get_context(self.APPLICATION_PATH_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_application_main_package_path()
        return self.get_context(self.APPLICATION_PATH_CONTEXT_KEY)

    def get_pyrin_root_path(self):
        """
        gets pyrin root path in which pyrin package is located.

        :rtype: str
        """

        result = self.get_context(self.ROOT_PYRIN_PATH_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_pyrin_root_path()
        return self.get_context(self.ROOT_PYRIN_PATH_CONTEXT_KEY)

    def get_application_root_path(self):
        """
        gets the application root path in which application package is located.

        :rtype: str
        """

        result = self.get_context(self.ROOT_APPLICATION_PATH_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_application_root_path()
        return self.get_context(self.ROOT_APPLICATION_PATH_CONTEXT_KEY)

    def get_pyrin_main_package_path(self):
        """
        gets pyrin main package path.

        :rtype: str
        """

        result = self.get_context(self.PYRIN_PATH_CONTEXT_KEY, default=None)
        if result is not None:
            return result

        self._resolve_pyrin_main_package_path()
        return self.get_context(self.PYRIN_PATH_CONTEXT_KEY)

    def get_working_directory(self):
        """
        gets working directory path of application.

        working directory is where the root application and test package are resided.
        this is required when application starts from any of test applications.
        then we should move root path up, to the correct root to be able to
        include real application packages too.
        if the application has been started from real application, this method
        returns the same result as `get_application_root_path()` method.

        :rtype: str
        """

        return packaging_services.get_working_directory(self.get_application_root_path())

    def get_configs(self):
        """
        gets a shallow copy of application's configuration dictionary.

        :rtype: dict
        """

        return self.config.copy()

    def _resolve_settings_path(self, **options):
        """
        resolves the application settings path.

        the resolved path will be accessible by `SETTINGS_CONTEXT_KEY`
        inside application context.

        :keyword str settings_directory: settings directory name.
                                         if not provided, defaults to `settings`.
        """

        directory = options.get('settings_directory', 'settings')
        directory = os.path.split(directory)
        main_package_path = self.get_application_main_package_path()
        settings_path = os.path.join(main_package_path, *directory)
        settings_path = os.path.abspath(settings_path)

        if not os.path.isdir(settings_path):
            print_warning('Application settings path [{path}] does not exist. '
                          'pyrin default settings will be used. you could change '
                          'any of default setting files inside [{path}] on your preference. '
                          'DO NOT use pyrin default settings in production!'
                          .format(path=settings_path))

        self.add_context(self.SETTINGS_CONTEXT_KEY, settings_path)

    def _resolve_default_settings_path(self):
        """
        resolves the pyrin default settings path.

        the resolved path will be accessible by `PYRIN_DEFAULT_SETTINGS_CONTEXT_KEY`
        inside application context.
        """

        pyrin_main_package_path = self.get_pyrin_main_package_path()
        settings_path = os.path.join(pyrin_main_package_path, 'settings', 'default')
        settings_path = os.path.abspath(settings_path)
        self.add_context(self.PYRIN_DEFAULT_SETTINGS_CONTEXT_KEY, settings_path)

    def _resolve_migrations_path(self, **options):
        """
        resolves the application migrations path.

        the resolved path will be accessible by `MIGRATIONS_CONTEXT_KEY`
        inside application context.

        :keyword str migrations_directory: migrations directory name.
                                           if not provided, defaults to `migrations`.
        """

        directory = options.get('migrations_directory', 'migrations')
        directory = os.path.split(directory)
        main_package_path = self.get_application_main_package_path()
        migrations_path = os.path.join(main_package_path, *directory)
        migrations_path = os.path.abspath(migrations_path)

        self.add_context(self.MIGRATIONS_CONTEXT_KEY, migrations_path)

    def _resolve_locale_path(self, **options):
        """
        resolves the application locale path.

        the resolved path will be accessible by `LOCALE_CONTEXT_KEY`
        inside application context.

        :keyword str locale_directory: locale directory name.
                                       if not provided, defaults to `locale`.
        """

        directory = options.get('locale_directory', 'locale')
        directory = os.path.split(directory)
        main_package_path = self.get_application_main_package_path()
        locale_path = os.path.join(main_package_path, *directory)
        locale_path = os.path.abspath(locale_path)

        self.add_context(self.LOCALE_CONTEXT_KEY, locale_path)

    def _resolve_application_main_package_path(self, **options):
        """
        resolves the application main package path.

        it registers it in application context with `APPLICATION_PATH_CONTEXT_KEY` key.
        """

        main_package_path = None
        if self._import_name is None:
            main_package_path = path_utils.get_main_package_path(self.__module__)
        else:
            main_package_path = path_utils.get_package_path(self._import_name)

        self.add_context(self.APPLICATION_PATH_CONTEXT_KEY, main_package_path)

    def _resolve_pyrin_main_package_path(self, **options):
        """
        resolves pyrin main package path.

        it registers it in application context with `PYRIN_PATH_CONTEXT_KEY` key.
        """

        pyrin_main_package = path_utils.get_pyrin_main_package_path()
        self.add_context(self.PYRIN_PATH_CONTEXT_KEY, pyrin_main_package)

    def _resolve_pyrin_root_path(self, **options):
        """
        resolves pyrin root path.

        it registers it in application context with `ROOT_PYRIN_PATH_CONTEXT_KEY` key.
        """

        main_package_path = self.get_pyrin_main_package_path()
        root_path = os.path.join(main_package_path, '..')
        root_path = os.path.abspath(root_path)
        self.add_context(self.ROOT_PYRIN_PATH_CONTEXT_KEY, root_path)

    def _resolve_application_root_path(self, **options):
        """
        resolves application root path.

        it registers it in application context with `ROOT_APPLICATION_PATH_CONTEXT_KEY` key.
        """

        main_package_path = self.get_application_main_package_path()
        root_path = os.path.join(main_package_path, '..')
        root_path = os.path.abspath(root_path)
        self.add_context(self.ROOT_APPLICATION_PATH_CONTEXT_KEY, root_path)

    def _load_environment_variables(self):
        """
        loads all environment variables defined in a `.env` file.

        it must be in application root path. if the
        file does not exist, it will be ignored.
        """

        root_path = self.get_application_root_path()
        env_file = os.path.join(root_path, '.env')

        if not os.path.isfile(env_file):
            print_warning('Could not find ".env" file in application root path [{root_path}].'
                          .format(root_path=root_path))
            return

        dotenv.load_dotenv(env_file)

    def process_response(self, response):
        """
        this method is overridden to add required attributes into response object.

        :param CoreResponse response: response object.

        :rtype: CoreResponse
        """

        client_request = session_services.get_current_request()
        response.request_date = client_request.request_date
        response.request_id = client_request.request_id
        response.user = session_services.get_current_user()

        return super().process_response(response)

    def full_dispatch_request(self):
        """
        dispatches the request and on top of that performs request pre and postprocessing.

        as well as http exception catching and error handling.
        this method has been overridden to log before and after request dispatching.
        """

        response = None
        client_request = session_services.get_current_request()
        process_start_time = time()
        logging_services.info('Request received with params: [{params}] '
                              'and headers: [{headers}].',
                              interpolation_data=
                              dict(params=self._get_request_data_for_logging(client_request),
                                   headers=client_request.headers))
        try:
            self._validate_request(client_request)
        except Exception as error:
            logging_services.exception(str(error))
            response = response_services.make_exception_response(error)
            response = self.make_response(response)

        if response is None:
            try:
                self._authenticate(client_request)
            except Exception as error:
                logging_services.exception(str(error))

            response = super().full_dispatch_request()

        response = self._finalize_transaction(response)

        process_end_time = time()
        logging_services.info('Request executed in [{time} ms].'
                              .format(time='{:0.3f}'
                                      .format((process_end_time - process_start_time) * 1000)))

        logging_services.debug('Response [{response}] returned with result: [{result}] '
                               'and headers: [{headers}].',
                               interpolation_data=
                               dict(response=response,
                                    result=self._get_response_data_for_logging(response),
                                    headers=response.headers))

        return response

    def finalize_request(self, rv, from_error_handler=False):
        """
        given the return value from a view function this finalizes the request.

        by converting it into a response and invoking the postprocessing functions.
        this is invoked for both normal request dispatching as well as error handlers.

        because this means that it might be called as a result of a failure a special
        safe mode is available which can be enabled with the `from_error_handler` flag.
        if enabled, failures in response processing will be logged and otherwise ignored.

        this method is overridden to inject custom response headers using application hook.

        :param object | tuple | CoreResponse rv: response from view function or error handlers.

        :param bool from_error_handler: specifies that this method is called as a result
                                        of a failure. defaults to False if not provided.

        :rtype: CoreResponse
        """

        body, status_code, headers = response_services.unpack_response(rv)

        extra_headers = self.headers_class()
        client_request = session_services.get_current_request()
        self._provide_response_headers(extra_headers, client_request.endpoint,
                                       status_code, client_request.method,
                                       url=client_request.path,
                                       user=client_request.user)
        extra_headers.extend(headers or {})
        response = response_services.pack_response(body, status_code, extra_headers)

        return super().finalize_request(response, from_error_handler=from_error_handler)

    def _get_request_data_for_logging(self, request):
        """
        gets the request data for logging.

        if request content length is larger than allowed value, it will be ignored.

        :param CoreRequest request: request instance.

        :rtype: dict
        """

        max_length = config_services.get_active('logging', 'max_request_size')
        if request.safe_content_length > max_length:
            return 'Request payload [{size} bytes] is too large for logging.' \
                .format(size=request.safe_content_length)

        return request.get_inputs(silent=True)

    def _get_response_data_for_logging(self, response):
        """
        gets the response data for logging.

        if response content length is larger than allowed value, it will be ignored.

        :param CoreResponse response: response instance.

        :rtype: dict | object
        """

        max_length = config_services.get_active('logging', 'max_response_size')
        if response.safe_content_length > max_length:
            return 'Response payload [{size} bytes] is too large for logging.' \
                .format(size=response.safe_content_length)

        log_all_types = config_services.get_active('logging', 'log_all_response_types')
        if response.content_type != MIMETypeEnum.JSON and \
                log_all_types is not True:
            return 'Response payload type [{content_type}] is ignored for logging.' \
                .format(content_type=response.content_type)

        return response.original_data

    def _set_component_attributes(self, old_instance, new_instance):
        """
        replaces required component attributes from old instance into new instance.

        it will replace all list and dict attributes from old instance into new instance.
        all the attributes which their name starts with two underscores (private attributes)
        will also be replaced from old instance into new instance.

        :param Component old_instance: old component instance to get attributes from.
        :param Component new_instance: new component instance to set its attributes.

        :rtype: Component
        """

        if old_instance is None or new_instance is None:
            return new_instance

        all_attributes = vars(old_instance)
        required_attributes = DTO()
        for attribute_name in all_attributes:
            if self._should_fill_from_parent(attribute_name,
                                             all_attributes[attribute_name]) is True:
                required_attributes[attribute_name] = all_attributes[attribute_name]

        return misc_utils.set_attributes(new_instance, **required_attributes)

    def _should_fill_from_parent(self, name, value):
        """
        gets a value indicating that given attribute value must be filled from parent.

        it is used on initializing subclassed managers (components) in extended packages.
        all list and dict values will result in True.
        all the attributes which their name starts with two underscores (private attributes)
        will also result in True.
        other attributes result in False.

        :param str name: attribute name to be checked.
        :param object value: attribute value to be checked.

        :rtype: bool
        """

        if '__' in name:
            return True

        return isinstance(value, (list, dict))

    def _after_application_loaded(self):
        """
        this method will call `after_application_loaded` method of all registered hooks.
        """

        for hook in self._get_hooks():
            hook.after_application_loaded()

    def _application_initialized(self):
        """
        this method will call `application_initialized` method of all registered hooks.
        """

        for hook in self._get_hooks():
            hook.application_initialized()

    def get_application_name(self):
        """
        gets the application name.

        it is actually the application main package name.
        first, it gets the import name of application if available.
        otherwise gets the first part of application package name

        :rtype: str
        """

        return self._import_name or path_utils.get_main_package_name(self.__module__)

    def _prepare_termination(self, signal_number):
        """
        prepares for termination.

        :param int signal_number: signal number that caused termination.
        """

        self._set_status(ApplicationStatusEnum.TERMINATED)

    def _application_status_changed(self, old_status, new_status):
        """
        this method will call `application_status_changed` method of all registered hooks.

        :param str old_status: old application status.
        :param str new_status: new application status.

        :enum status:
            INITIALIZING = 'Initializing'
            LOADING = 'Loading'
            READY = 'Ready'
            RUNNING = 'Running'
            TERMINATED = 'Terminated'
        """

        for hook in self._get_hooks():
            hook.application_status_changed(old_status, new_status)

    def _before_application_run(self):
        """
        this method will call `before_application_run` method of all registered hooks.

        note that this method will not get called when
        application starts in scripting mode.
        """

        for hook in self._get_hooks():
            hook.before_application_run()

    def _prepare_runtime_data(self):
        """
        this method will call `prepare_runtime_data` method of all registered hooks.

        this method will commit any changes of each hook to database, so you should
        not commit anything in the hooks. if you do commit manually, unexpected
        behaviors may occur.

        note that this method will not get called when application starts in scripting mode.
        """

        for hook in self._get_hooks():
            with atomic_context(expire_on_commit=True):
                hook.prepare_runtime_data()

    def _provide_response_headers(self, headers, endpoint,
                                  status_code, method, **options):
        """
        this method will call `provide_response_headers` method of all registered hooks.

        :param dict | Headers headers: current response headers.

        :param str endpoint: the endpoint of the route that
                             handled the current request.
                             by default, it is the fully qualified
                             name of the view function.

        :param int status_code: response status code.
                                it could be None if not provided.

        :param str method: the http method of current request.

        :keyword str url: the url of the route that handled this request.

        :keyword user: the user of current request.
                       it could be None.
        """

        for hook in self._get_hooks():
            hook.provide_response_headers(headers, endpoint,
                                          status_code, method, **options)

    def _finalize_transaction(self, response, **options):
        """
        this method will call `finalize_transaction` of all registered hooks.

        :param CoreResponse response: response object.

        :rtype: CoreResponse
        """

        result_response = response
        for hook in self._get_hooks():
            try:
                result = hook.finalize_transaction(result_response, **options)
                if result is not None:
                    if not isinstance(result, self.response_class):
                        result = self.make_response(result)
                    result_response = result
            except Exception as error:
                logging_services.exception(str(error))

        return result_response

    def _validate_request(self, request, **options):
        """
        this method will call `validate_request` method of all registered hooks.

        :param CoreRequest request: current request instance.
        """

        for hook in self._get_hooks():
            hook.validate_request(request, **options)

    def get_application_version(self):
        """
        gets application version.

        :rtype: str
        """

        return self._version

    def get_pyrin_version(self):
        """
        gets pyrin version.

        :rtype: str
        """

        return pyrin.__version__
