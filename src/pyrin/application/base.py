# -*- coding: utf-8 -*-
"""
application base module.
"""

import os.path

from time import time

from dotenv import load_dotenv as load_dotenv_
from flask import Flask, request
from flask.app import setupmethod
from flask.ctx import has_request_context

import pyrin.packaging.services as packaging_services
import pyrin.configuration.services as config_services
import pyrin.security.authentication.services as authentication_services
import pyrin.security.session.services as session_services
import pyrin.logging.services as logging_services
import pyrin.database.model.services as model_services
import pyrin.utils.misc as misc_utils
import pyrin.utils.path as path_utils

from pyrin.application.container import _set_app
from pyrin.api.router.handlers.protected import ProtectedRoute
from pyrin.application.enumerations import ApplicationStatusEnum
from pyrin.application.hooks import ApplicationHookBase
from pyrin.application.mixin import SignalMixin
from pyrin.converters.json.decoder import CoreJSONDecoder
from pyrin.converters.json.encoder import CoreJSONEncoder
from pyrin.converters.serializer.entity import CoreEntitySerializer
from pyrin.converters.serializer.keyed_tuple import CoreKeyedTupleSerializer
from pyrin.core.context import DTO, Manager
from pyrin.core.globals import LIST_TYPES
from pyrin.core.mixin import HookMixin
from pyrin.packaging import PackagingPackage
from pyrin.packaging.component import PackagingComponent
from pyrin.application.context import CoreResponse, CoreRequest, ApplicationContext, \
    ApplicationComponent, ApplicationSingletonMeta
from pyrin.application.context import Component
from pyrin.settings.static import DEFAULT_COMPONENT_KEY
from pyrin.utils.custom_print import print_warning
from pyrin.utils.dictionary import make_key_upper
from pyrin.application.exceptions import DuplicateContextKeyError, InvalidComponentTypeError, \
    InvalidComponentIDError, DuplicateComponentIDError, DuplicateRouteURLError, \
    InvalidRouteFactoryTypeError, ApplicationSettingsPathNotExistedError, \
    InvalidApplicationStatusError, ApplicationInScriptingModeError, ComponentAttributeError, \
    ApplicationIsNotSubclassedError


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

    url_rule_class = ProtectedRoute
    response_class = CoreResponse
    request_class = CoreRequest
    json_decoder = CoreJSONDecoder
    json_encoder = CoreJSONEncoder
    entity_serializer = CoreEntitySerializer
    keyed_tuple_serializer = CoreKeyedTupleSerializer
    _hook_type = ApplicationHookBase

    def __init__(self, **options):
        """
        initializes an instance of Application.

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
                                      scripting mode. some application hooks will not
                                      get fired when the app runs in scripting mode.
                                      defaults to False, if not provided.

        :keyword str settings_directory: settings directory name.
                                         if not provided, defaults to `settings`.

        :keyword str migrations_directory: migrations directory name.
                                           if not provided, defaults to `migrations`.

        :keyword str locale_directory: locale directory name.
                                       if not provided, defaults to `locale`.
        """

        self._assert_is_subclassed()

        self.__status = ApplicationStatusEnum.INITIALIZING
        self._scripting_mode = options.pop('scripting_mode', False)

        # we should pass `static_folder=None` to prevent flask from
        # adding static route on startup, then we register required static routes
        # through a correct mechanism later.
        super().__init__(self.get_application_name(), static_folder=None, **options)

        # Flask does not call 'super()' in its '__init__()' method.
        # so we have to start initialization of other parents manually.
        HookMixin.__init__(self, **options)

        self._context = ApplicationContext()
        self._components = ApplicationComponent()

        # we should register some packages manually because they are referenced
        # in `application.base` module and could not be loaded automatically
        # because packaging package will not handle them.
        self._register_required_components()

        # setting the application instance in application container module.
        _set_app(self)

        # we should load application at this stage to be able to perform pytest
        # tests after application has been fully loaded. because if we call
        # application.run(), we could not continue execution of other codes.
        self._load(**options)
        self._set_status(ApplicationStatusEnum.RUNNING)

    def _assert_is_subclassed(self):
        """
        asserts that current application instance is subclassed from
        `Application` class and is not a direct instance of `Application` itself.

        :raises ApplicationIsNotSubclassedError: application is not subclassed error.
        """

        if type(self) == Application:
            raise ApplicationIsNotSubclassedError('Current application instance is a direct '
                                                  'instance of "Application". you must subclass '
                                                  'from "Application" in your project and create '
                                                  'an instance of that class to run your '
                                                  'application. this is needed for pyrin to be '
                                                  'able to resolve different paths correctly.')

    def is_scripting_mode(self):
        """
        gets a value indicating that application has been started in scripting mode.
        some application hooks will not fire in this mode. like 'before_application_start'.
        """

        return self._scripting_mode

    @setupmethod
    def _register_required_components(self):
        """
        registers required components that the Application needs to
        reference to them immediately.
        this type of components could not be registered using @component decorator,
        because they will be referenced before Application instance gets initialized.

        note that implementation-wise, application package should depend on other
        packages services as few as possible, so be careful if you needed some external
        packages services inside application package, probably it would be better to
        change your design that enforces the application to use other packages services.
        """

        self.register_component(self.packaging_component_class(
            PackagingPackage.COMPONENT_NAME))

    def _set_status(self, status):
        """
        sets the application status.
        status must be from ApplicationStatusEnum.

        :param str status: application status.

        :note status:
            INITIALIZING = 'Initializing'
            LOADING = 'Loading'
            RUNNING = 'Running'
            TERMINATED = 'Terminated'

        raises InvalidApplicationStatusError: invalid application status error.
        """

        if status not in ApplicationStatusEnum:
            raise InvalidApplicationStatusError('Application status [{state}] is not valid.'
                                                .format(state=status))

        old_status = self.__status
        self.__status = status

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

    def get_context(self, key):
        """
        gets the application context value that belongs to given key.

        :param str key: key for requested application context.

        :returns: related value to given key.
        """

        return self._context[key]

    @setupmethod
    def register_component(self, component, **options):
        """
        registers given application component or replaces the existing one
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
                                            'an instance of Manager. each component '
                                            'class must be subclassed from its respective '
                                            'manager class of the same package and that '
                                            'manager class must be subclassed from Manager.'
                                            .format(component=str(component)))

        if not isinstance(component, Component):
            raise InvalidComponentTypeError('Input parameter [{component}] is not '
                                            'an instance of Component.'
                                            .format(component=str(component)))

        if not isinstance(component.get_id(), tuple) or \
                len(component.get_id()[0].strip()) == 0:
            raise InvalidComponentIDError('Component [{component}] has '
                                          'not a valid component id.'
                                          .format(component=str(component)))

        # checking whether is there any registered component with the same id.
        if component.get_id() in self._components.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicateComponentIDError('There is another registered component with '
                                                'id [{id}] but "replace" option is not set, so '
                                                'component [{instance}] could not be registered.'
                                                .format(id=component.get_id(),
                                                        instance=str(component)))

            old_instance = self._components[component.get_id()]

            # we should update all list and dict attributes and also those that have
            # three consecutive underscores in their names of new component with values
            # from old_instance to prevent loss of any attribute value (for example values
            # that has been added using decorators).
            # this has an obvious caveat, and it is that child classes could not do
            # any customizations on these attributes in their `__init__` method.
            component = self._set_component_attributes(old_instance, component)

            print_warning('Component [{old_instance}] is going to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(component)))

        self._components[component.get_id()] = component

    def remove_component(self, component_id):
        """
        removes application component with given id.

        :param tuple component_id: component id to be removed.
        :type component_id: tuple(str, object)

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
            with request:
                return request

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
        note that if application is in any state other than `RUNNING`,
        it always returns the default component key.

        :rtype: object
        """

        # before application reaches the `RUNNING` state,
        # we should always use the default component key.
        if self.get_status() != ApplicationStatusEnum.RUNNING:
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
        self._resolve_all_paths(**options)
        self._load_environment_variables()

        packaging_services.load_components(**options)

        # we should call this method after loading components
        # to be able to use configuration package.
        self._load_configs(**options)

        # calling `after_application_loaded` method of all registered hooks.
        self._after_application_loaded()

        # calling `before_application_start` method of all registered hooks.
        # this hook should not be called when the app is in scripting mode.
        if self.is_scripting_mode() is False:
            self._before_application_start()

    def _resolve_all_paths(self, **options):
        """
        resolves all required paths for application.
        """

        self._resolve_pyrin_main_package_path(**options)
        self._resolve_application_main_package_path(**options)
        self._resolve_pyrin_root_path(**options)
        self._resolve_application_root_path(**options)
        self._resolve_settings_path(**options)
        self._resolve_migrations_path(**options)
        self._resolve_locale_path(**options)

    def _load_configs(self, **options):
        """
        loads all configurations related to application package.
        """

        config_services.load_configurations(*self.CONFIG_STORES, **options)
        for store_name in self.CONFIG_STORES:
            config_dict = config_services.get_all(store_name, **options)
            self.configure(config_dict)

    def _configure(self, config_store):
        """
        configures the application with given dict.
        all keys will be converted to uppercase for flask compatibility.

        :param dict config_store: a dictionary containing configuration key/values.
        """

        upper_dict = make_key_upper(config_store)
        self.config.update(upper_dict)

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

        :param str host: the hostname to listen on. Set this to `0.0.0.0` to
                         have the server available externally as well. defaults to
                         `127.0.0.1` or the host in the `SERVER_NAME`
                         config variable if present.

        :param int port: the port of the webserver. defaults to `5000` or the
                         port defined in the `SERVER_NAME` config variable if present.

        :param bool debug: if given, enable or disable debug mode.

        :param bool load_dotenv: load the nearest `.env` and `.flaskenv`
                                 files to set environment variables. will also change the working
                                 directory to the directory containing the first file found.

        :raises ApplicationInScriptingModeError: application in scripting mode error.
        """

        if self.is_scripting_mode() is True:
            raise ApplicationInScriptingModeError('Application has been initialized in '
                                                  'scripting mode, so it could not be run.')

        super().run(host, port, debug, load_dotenv, **options)

    def dispatch_request(self):
        """
        does the request dispatching. matches the URL and returns the
        return value of the view or error handlers. this does not have to
        be a response object. in order to convert the return value to a
        proper response object, call `make_response` function.

        :raises AuthenticationFailedError: authentication failed error.
        """

        # we have to override whole `dispatch_request` method to be able to customize it,
        # because of flask design that everything is embedded inside
        # the `dispatch_request` method.

        client_request = session_services.get_current_request()
        if client_request.routing_exception is not None:
            self.raise_routing_exception(client_request)

        route = client_request.url_rule

        # if we provide automatic options for this URL and the
        # request came with the OPTIONS method, reply automatically.
        if getattr(route, 'provide_automatic_options', False) \
           and client_request.method == 'OPTIONS':
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

    def make_response(self, rv):
        """
        converts the return value from a view function
        to an instance of `CoreResponse`.

        note that the `rv` value before passing to base method must
        be a `tuple`, `dict`, `str` or `CoreResponse`. otherwise
        the value will not be json serialized and it causes an error.

        :param object rv: the return value from the view function.

        :rtype: CoreResponse
        """

        rv = self._convert_result(rv)

        if rv is None:
            rv = DTO()

        # we could not return a list as response, so we wrap the
        # result in a dict when we want to return a list.
        if isinstance(rv, list):
            rv = DTO(items=rv)

        # we should wrap all single values into a dict before returning it to client.
        if not isinstance(rv, (tuple, dict, CoreResponse)):
            rv = DTO(value=rv)

        return super().make_response(rv)

    def _convert_result(self, rv):
        """
        converts the return value if needed.
        this method could be overridden in subclasses.

        :param object rv: the return value from the view function.

        :rtype: object
        """

        if isinstance(rv, list) and len(rv) > 0:
            if model_services.is_abstract_keyed_tuple(rv[0]):
                rv = self.keyed_tuple_serializer.serialize_list(rv)
            elif model_services.is_core_entity(rv[0]):
                rv = self.entity_serializer.serialize_list(rv)

        elif model_services.is_abstract_keyed_tuple(rv):
            rv = self.keyed_tuple_serializer.serialize(rv)

        elif model_services.is_core_entity(rv):
            rv = self.entity_serializer.serialize(rv)

        return rv

    @setupmethod
    def add_url_rule(self, rule, endpoint=None, view_func=None,
                     provide_automatic_options=None, **options):
        """
        connects a url rule. if a view_func is provided it will be registered with the endpoint.
        if there is another rule with the same url and `replace=True` option is provided,
        it will be replaced, otherwise an error will be raised.

        :param str rule: the url rule as string.

        :param str endpoint: the endpoint for the registered url rule.
                             pyrin itself assumes the url rule as endpoint.

        :param callable view_func: the function to call when serving a request to the
                                   provided endpoint.

        :param bool provide_automatic_options: controls whether the `OPTIONS` method should be
                                               added automatically.
                                               this can also be controlled by setting the
                                               `view_func.provide_automatic_options = False`
                                               before adding the rule.

        :keyword tuple(str) methods: http methods that this rule should handle.
                                     if not provided, defaults to `GET`.

        :keyword tuple(PermissionBase) permissions: tuple of all required permissions
                                                    to access this route's resource.

        :keyword bool login_required: specifies that this route could not be accessed
                                      if the requester has not a valid token.
                                      defaults to True if not provided.

        :keyword bool replace: specifies that this route must replace
                               any existing route with the same url or raise
                               an error if not provided. defaults to False.

        :raises DuplicateRouteURLError: duplicate route url error.
        """

        methods = options.get('methods', ())
        if not isinstance(methods, LIST_TYPES):
            options.update(methods=(methods,))

        replace = options.get('replace', False)

        # setting endpoint to url rule instead of view function name,
        # to be able to have the same function names on different url rules.
        if endpoint is None:
            endpoint = rule

        # checking whether is there any registered route with the same url.
        old_rule = None
        for rule_item in self.url_map.iter_rules(endpoint=None):
            if rule_item.rule == rule:
                old_rule = rule_item
                break

        if old_rule is not None:
            if replace is True:
                self.url_map._rules.remove(old_rule)
                if old_rule.endpoint in self.view_functions.keys():
                    self.view_functions.pop(old_rule.endpoint)
                if old_rule.endpoint in self.url_map._rules_by_endpoint.keys():
                    self.url_map._rules_by_endpoint.pop(old_rule.endpoint)

                print_warning('Registered route for url [{url}] is '
                              'going to be replaced by a new route.'
                              .format(url=rule))
            else:
                raise DuplicateRouteURLError('There is another registered route with the '
                                             'same url [{url}], but "replace" option is not '
                                             'set, so the new route could not be registered.'
                                             .format(url=rule))

        # we have to put `view_function=view_func` into options to be able to deliver it
        # to route initialization in the super method. that's because of flask design
        # that does not forward all params to inner method calls. and this is the less
        # ugly way in comparison to overriding the whole `add_url_rule` function.
        options.update(view_function=view_func)

        super().add_url_rule(rule, endpoint, view_func,
                             provide_automatic_options, **options)

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
                                               .format(factory=str(factory)))

        print_warning('Registered route factory [{old_factory}] is '
                      'going to be replaced by a new route factory [{new_factory}].'
                      .format(old_factory=str(self.url_rule_class),
                              new_factory=str(factory)))

        self.url_rule_class = factory

    def get_current_route_factory(self):
        """
        gets current route factory in use.

        :rtype: callable
        """

        return self.url_rule_class

    def get_settings_path(self):
        """
        gets the application settings path.

        :rtype: str
        """

        return self.get_context(self.SETTINGS_CONTEXT_KEY)

    def get_migrations_path(self):
        """
        gets the application migrations path.

        :rtype: str
        """

        return self.get_context(self.MIGRATIONS_CONTEXT_KEY)

    def get_locale_path(self):
        """
        gets the application locale path.

        :rtype: str
        """

        return self.get_context(self.LOCALE_CONTEXT_KEY)

    def get_application_main_package_path(self):
        """
        gets the application main package path.

        :rtype: str
        """

        return self.get_context(self.APPLICATION_PATH_CONTEXT_KEY)

    def get_pyrin_root_path(self):
        """
        gets pyrin root path in which pyrin package is located.

        :rtype: str
        """

        return self.get_context(self.ROOT_PYRIN_PATH_CONTEXT_KEY)

    def get_application_root_path(self):
        """
        gets the application root path in which application package is located.

        :rtype: str
        """

        return self.get_context(self.ROOT_APPLICATION_PATH_CONTEXT_KEY)

    def get_pyrin_main_package_path(self):
        """
        gets pyrin main package path.

        :rtype: str
        """

        return self.get_context(self.PYRIN_PATH_CONTEXT_KEY)

    def get_configs(self):
        """
        gets a shallow copy of application's configuration dictionary.

        :rtype: dict
        """

        return self.config.copy()

    def _resolve_settings_path(self, **options):
        """
        resolves the application settings path. the resolved path will
        be accessible by `SETTINGS_CONTEXT_KEY` inside application context.

        :keyword str settings_directory: settings directory name.
                                         if not provided, defaults to `settings`.

        :raises ApplicationSettingsPathNotExistedError: application settings path
                                                        not existed error.
        """

        main_package_path = self.get_application_main_package_path()

        settings_path = '{main_package_path}/{settings_directory}' \
                        .format(main_package_path=main_package_path,
                                settings_directory=options.get('settings_directory',
                                                               'settings'))
        settings_path = os.path.abspath(settings_path)

        if not os.path.isdir(settings_path):
            raise ApplicationSettingsPathNotExistedError('Settings path [{path}] does not exist.'
                                                         .format(path=settings_path))

        self.add_context(self.SETTINGS_CONTEXT_KEY, settings_path)

    def _resolve_migrations_path(self, **options):
        """
        resolves the application migrations path. the resolved path will
        be accessible by `MIGRATIONS_CONTEXT_KEY` inside application context.

        :keyword str migrations_directory: migrations directory name.
                                           if not provided, defaults to `migrations`.
        """

        main_package_path = self.get_application_main_package_path()

        migrations_path = '{main_package_path}/{migrations_directory}' \
                          .format(main_package_path=main_package_path,
                                  migrations_directory=options.get('migrations_directory',
                                                                   'migrations'))
        migrations_path = os.path.abspath(migrations_path)

        self.add_context(self.MIGRATIONS_CONTEXT_KEY, migrations_path)

    def _resolve_locale_path(self, **options):
        """
        resolves the application locale path. the resolved path will
        be accessible by `LOCALE_CONTEXT_KEY` inside application context.

        :keyword str locale_directory: locale directory name.
                                       if not provided, defaults to `locale`.
        """

        main_package_path = self.get_application_main_package_path()

        locale_path = '{main_package_path}/{locale_directory}' \
                      .format(main_package_path=main_package_path,
                              locale_directory=options.get('locale_directory',
                                                           'locale'))
        locale_path = os.path.abspath(locale_path)

        self.add_context(self.LOCALE_CONTEXT_KEY, locale_path)

    def _resolve_application_main_package_path(self, **options):
        """
        resolves the application main package path and registers it
        in application context with `APPLICATION_PATH_CONTEXT_KEY` key.
        """

        main_package_path = path_utils.get_main_package_path(self.__module__)
        self.add_context(self.APPLICATION_PATH_CONTEXT_KEY, main_package_path)

    def _resolve_pyrin_main_package_path(self, **options):
        """
        resolves pyrin main package path and registers it
        in application context with `PYRIN_PATH_CONTEXT_KEY` key.
        """

        pyrin_main_package = path_utils.get_pyrin_main_package_path()
        self.add_context(self.PYRIN_PATH_CONTEXT_KEY, pyrin_main_package)

    def _resolve_pyrin_root_path(self, **options):
        """
        resolves pyrin root path and registers it in application
        context with `ROOT_PYRIN_PATH_CONTEXT_KEY` key.
        """

        main_package_path = self.get_pyrin_main_package_path()
        root_path = os.path.join(main_package_path, '..')
        root_path = os.path.abspath(root_path)
        self.add_context(self.ROOT_PYRIN_PATH_CONTEXT_KEY, root_path)

    def _resolve_application_root_path(self, **options):
        """
        resolves application root path and registers it in application
        context with `ROOT_APPLICATION_PATH_CONTEXT_KEY` key.
        """

        main_package_path = self.get_application_main_package_path()
        root_path = os.path.join(main_package_path, '..')
        root_path = os.path.abspath(root_path)
        self.add_context(self.ROOT_APPLICATION_PATH_CONTEXT_KEY, root_path)

    def _load_environment_variables(self):
        """
        loads all environment variables defined in a `.env` file in application
        root path. if the file does not exist, it will be ignored.
        """

        root_path = self.get_application_root_path()
        env_file = os.path.join(root_path, '.env')

        if not os.path.isfile(env_file):
            print_warning('Could not find ".env" file in application root path [{root_path}].'
                          .format(root_path=root_path))
            return

        load_dotenv_(env_file)

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
        dispatches the request and on top of that performs request pre and
        postprocessing as well as http exception catching and error handling.
        this method has been overridden to log before and after request dispatching.
        """

        client_request = session_services.get_current_request()
        try:
            self._authenticate(client_request)

        except Exception as error:
            logging_services.exception(str(error))

        process_start_time = time()
        logging_services.info('request received with params: [{params}]'
                              .format(params=client_request.get_inputs(silent=True)))

        response = super().full_dispatch_request()

        process_end_time = time()
        logging_services.info('request executed in [{time} ms].'
                              .format(time='{:0.3f}'
                                      .format((process_end_time - process_start_time) * 1000)))

        logging_services.debug('[{response}] returned with result: [{result}]'
                               .format(response=response,
                                       result=response.get_data(as_text=True)))

        return response

    def _set_component_attributes(self, old_instance, new_instance):
        """
        replaces all list and dict attributes from old instance into new instance.
        all the attributes which their name starts with three underscores will also
        be replaced from old instance into new instance.

        :param Component old_instance: old component instance to get attributes from.
        :param Component new_instance: new component instance to set its attributes.

        :rtype: Component
        """

        if old_instance is None or new_instance is None:
            return new_instance

        all_attributes = vars(old_instance)
        required_attributes = DTO()
        for attribute_name in all_attributes.keys():
            if isinstance(all_attributes[attribute_name], (list, dict)) \
                    or '___' in attribute_name:
                required_attributes[attribute_name] = all_attributes[attribute_name]

        return misc_utils.set_attributes(new_instance, **required_attributes)

    def _after_application_loaded(self):
        """
        this method will call `after_application_loaded` method of all registered hooks.
        """

        for hook in self._get_hooks():
            hook.after_application_loaded()

    def _before_application_start(self):
        """
        this method will call `before_application_start` method of all registered hooks.
        """

        for hook in self._get_hooks():
            hook.before_application_start()

    def get_application_name(self):
        """
        gets the application name.

        :rtype: str
        """

        return path_utils.get_main_package_name(self.__module__)

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

        :note status:
            INITIALIZING = 'Initializing'
            LOADING = 'Loading'
            RUNNING = 'Running'
            TERMINATED = 'Terminated'
        """

        for hook in self._get_hooks():
            hook.application_status_changed(old_status, new_status)
