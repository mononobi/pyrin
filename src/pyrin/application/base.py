# -*- coding: utf-8 -*-
"""
application base module.
"""

import signal
import sys
import os.path

from time import time

from dotenv import load_dotenv as load_dotenv_
from flask import Flask, request
from flask.app import setupmethod

import pyrin.packaging.services as packaging_services
import pyrin.configuration.services as config_services
import pyrin.security.authentication.services as authentication_services
import pyrin.security.session.services as session_services
import pyrin.logging.services as logging_services

from pyrin import _set_app
from pyrin.api.router.handlers.protected import ProtectedRoute
from pyrin.application.enumerations import ApplicationStatusEnum
from pyrin.application.exceptions import DuplicateContextKeyError, InvalidComponentTypeError, \
    InvalidComponentIDError, DuplicateComponentIDError, DuplicateRouteURLError, \
    InvalidRouteFactoryTypeError, ApplicationSettingsPathNotExistedError, \
    InvalidApplicationStatusError
from pyrin.converters.json.decoder import CoreJSONDecoder
from pyrin.converters.json.encoder import CoreJSONEncoder
from pyrin.packaging import PackagingPackage
from pyrin.packaging.component import PackagingComponent
from pyrin.application.context import CoreResponse, CoreRequest, ApplicationContext, \
    ApplicationComponent
from pyrin.application.context import Component
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.settings.static import DEFAULT_COMPONENT_KEY
from pyrin.utils.custom_print import print_warning, print_error
from pyrin.utils.dictionary import make_key_upper
from pyrin.utils.path import resolve_application_root_path


class Application(Flask):
    """
    application class.
    server must initialize an instance of this class at startup.
    """

    # the application looks for these stores to configure itself.
    # they should be present in settings folder of the upper
    # level application.
    CONFIG_STORES = ['application',
                     'communication',
                     'environment']

    # settings path will be registered in application context with this key.
    SETTINGS_CONTEXT_KEY = 'settings_path'

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

    def __init__(self, import_name, **options):
        """
        initializes an instance of Application.

        :param str import_name: name of the main application package.

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
        """

        self.__status = ApplicationStatusEnum.INITIALIZING

        # we should pass `static_folder=None` to prevent flask from
        # adding static route on startup, then we register required static routes
        # through a correct mechanism later.
        super(Application, self).__init__(import_name, static_folder=None, **options)

        self._context = ApplicationContext()
        self._components = ApplicationComponent()

        # we should register some packages manually because they are referenced
        # in `application.base` module and could not be loaded automatically
        # because packaging package will not handle them.
        self._register_required_components()

        # setting the application instance in global 'pyrin' level variable.
        _set_app(self)

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

        :param int status: application status.

        raises InvalidApplicationStatusError: invalid application status error.
        """

        if not ApplicationStatusEnum.has_value(status):
            raise InvalidApplicationStatusError('Application status [{state}] is not valid.'
                                                .format(state=status))

        self.__status = status

    def get_status(self):
        """
        gets the application status.

        :rtype: int
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
                                           'context and `replace=True` option is not set, so '
                                           'the new value could not be added.'
                                           .format(key=key))

        self._context[key] = value

    def get_context(self, key):
        """
        gets the application context value that belongs to given key.

        :param str key: key for requested application context.

        :rtype: object
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
            print_warning('Component [{old_instance}] is going to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(component)))

        self._components[component.get_id()] = component

    def get_component(self, component_name, **options):
        """
        gets the specified application component.

        :param str component_name: component name.

        :raises InvalidComponentNameError: invalid component name error.

        :rtype: Component
        """

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
        with request as client_request:
            return client_request.component_custom_key

    def _load(self, **options):
        """
        loads application configs and components.
        """

        self._set_status(ApplicationStatusEnum.LOADING)
        self._load_environment_variables()
        self._resolve_settings_path()
        packaging_services.load_components(**options)

        # we should call this method after loading components
        # to be able to use configuration package.
        self._load_configs(**options)

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
        """

        self._load()
        self._set_status(ApplicationStatusEnum.RUNNING)
        super(Application, self).run(host, port, debug, load_dotenv, **options)

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
        return route.handle(client_request.inputs)

    def _authenticate(self, client_request):
        """
        authenticates given request.

        :param CoreRequest client_request: request to be authenticated.

        :raises AuthenticationFailedError: authentication failed error.
        """

        authentication_services.authenticate(client_request)

    def make_response(self, rv):
        """
        converts the return value from a view function to an instance of dict.
        if the return value is None, it returns an empty dict as return value.

        :param object rv: the return value from the view function.

        :rtype: object.
        """

        if rv is None:
            rv = {}

        return super(Application, self).make_response(rv)

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
        if not isinstance(methods, (tuple, list, set)):
            options.update(methods=(methods,))

        replace = options.get('replace', False)

        # setting endpoint to url rule instead of view function name,
        # to be able to have the same function names on different url rules.
        if endpoint is None:
            endpoint = rule

        # checking whether is there any registered route with the same url.
        old_rule = None
        for rule_item in self.url_map._rules:
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

        super(Application, self).add_url_rule(rule, endpoint, view_func,
                                              provide_automatic_options, **options)

    def terminate(self, **options):
        """
        terminates the application.
        this method should not be called directly.
        it is defined for cases that application has to
        be terminated for some unexpected reasons.

        :keyword int status: status code to use for application exit.
                             if not provided, status=0 will be used.
        """

        print_error('Terminating application [{name}].'.format(name=self.name))

        # forcing termination after 10 seconds.
        signal.alarm(10)
        self._set_status(ApplicationStatusEnum.TERMINATED)

        sys.exit(options.get('status', 0))

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

        self.url_rule_class = factory

    def get_settings_path(self):
        """
        gets the application settings path.

        :rtype: str
        """

        return self.get_context(self.SETTINGS_CONTEXT_KEY)

    def _resolve_settings_path(self, **options):
        """
        resolves the application settings path. the resolved path will
        be accessible by `self.SETTINGS_CONTEXT_KEY` inside application context.

        :keyword str settings_directory: settings directory name.
                                         if not provided, defaults to `settings`.

        :raises ApplicationSettingsPathNotExistedError: application settings path
                                                        not existed error.

        :rtype: str
        """

        main_package_path = self._resolve_application_main_package_path(**options)

        settings_path = '{main_package_path}/{settings_directory}' \
                        .format(main_package_path=main_package_path,
                                settings_directory=options.get('settings', 'settings'))

        if not os.path.isdir(settings_path):
            raise ApplicationSettingsPathNotExistedError('Settings path [{path}] does not exist.'
                                                         .format(path=settings_path))

        self.add_context(self.SETTINGS_CONTEXT_KEY, settings_path)

    def _resolve_application_main_package_path(self, **options):
        """
        resolves the application main package path.
        each derived class from Application, must override this method,
        and resolve it's own main package path.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _load_environment_variables(self):
        """
        loads all environment variables defined in a `.env` file in application
        root path. if the file does not exist, it will be ignored.
        """

        root_path = resolve_application_root_path()
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

        response.user = session_services.get_current_user()
        response.request_date = session_services.get_current_request().request_date
        response.request_id = session_services.get_current_request().request_id

        return super(Application, self).process_response(response)

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
            logging_services.exception('{client_request} - {message}'
                                       .format(message=str(error),
                                               client_request=client_request))

        process_start_time = time()
        logging_services.info('{client_request} received. '
                              'params: [{params}]'
                              .format(client_request=client_request,
                                      params=client_request.inputs))

        response = super(Application, self).full_dispatch_request()

        process_end_time = time()
        logging_services.info('{client_request} executed in [{time} ms].'
                              .format(client_request=client_request,
                                      time='{:0.3f}'
                                      .format((process_end_time - process_start_time) * 1000)))

        logging_services.debug('{response} returned. '
                               'result: [{result}]'
                               .format(response=response,
                                       result=response.get_data(as_text=True)))

        return response
