# -*- coding: utf-8 -*-
"""
application base module.
"""

import signal
import sys
import os.path

from time import time

from dotenv import load_dotenv as load_dotenv_
from flask.app import setupmethod

import pyrin.packaging.services as packaging_services
import pyrin.configuration.services as config_services
import pyrin.security.authentication.services as authentication_services
import pyrin.security.session.services as session_services
import pyrin.logging.services as logging_services

from pyrin.application.base import Application
from pyrin.application.enumerations import ApplicationStatusEnum
from pyrin.application.exceptions import DuplicateRouteURLError, \
    InvalidRouteFactoryTypeError, ApplicationSettingsPathNotExistedError
from pyrin.packaging import PackagingPackage
from pyrin.application.context import CoreResponse, CoreRequest
from pyrin.application.context import Component
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utils.custom_print import print_warning, print_error
from pyrin.utils.dictionary import make_key_upper
from pyrin.utils.path import resolve_application_root_path


class TestApplication(Application):
    """
    test application class.
    test server must initialize an instance of this class at startup.
    """

    def test_register_required_components(self):
        """
        asserts that all required components are registered.
        """

        packaging_component = self.get_component(PackagingPackage.COMPONENT_NAME)
        assert packaging_component is not None
        assert isinstance(packaging_component, self.packaging_component_class)

    def test_set_status(self):
        """
        asserts that application status will correctly set.
        """

        current_status = self.get_status()
        self._set_status(ApplicationStatusEnum.LOADING)
        assert self.get_status() == ApplicationStatusEnum.LOADING
        self._set_status(current_status)

    def test_add_context(self):
        """
        asserts that added context is available in application context.
        """

        self.add_context('fake_key', 'fake_value')
        assert self.get_context('fake_key') == 'fake_value'

    def test_register_component(self):
        """
        asserts that added component is available in application components.
        """

        fake_component = Component('fake_component')
        self.register_component(fake_component)
        assert self.get_component('fake_component') is not None
        assert self.get_component('fake_component') == fake_component

    def test_get_safe_current_request(self):
        """
        asserts that getting current request is safe and never fails.
        """

        current_request = self._get_safe_current_request()
        assert current_request is None or isinstance(current_request, CoreRequest)

    def test_load(self, **options):
        """
        asserts that application components has been loaded.
        """

        components = ['api.component',
                      'api.router.component',
                      'configuration.component',
                      'database.component',
                      'localization.component',
                      'logging.component',
                      'converters.deserializer.component',
                      'security.component',
                      'security.authentication.component',
                      'security.authorization.component',
                      'security.encryption.component',
                      'security.hashing.component',
                      'security.permission.component',
                      'security.session.component',
                      'security.token.component']

        for component in components:
            assert self.get_component(component) is not None

    def test_load_configs(self, **options):
        """
        asserts that application configurations are loaded correctly.
        """

        application_store = config_services.get_all('application')
        environment_store = config_services.get_active_section('environment')
        communication_store = config_services.get_active_section('communication')

        for key in application_store.keys():
            assert key.isupper() is True

        for key in environment_store.keys():
            assert key.isupper() is True

        for key in communication_store.keys():
            assert key.isupper() is True

        assert application_store.get('title') == 'tests'
        assert application_store.get('base_currency') == 'IRR'

        assert environment_store.get('env') == 'testing'
        assert environment_store.get('testing') is True

        assert communication_store.get('server_name') == 'localhost.localdomain:9083'
        assert communication_store.get('server_port') == 9083

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

        client_request = session_services.get_current_request()
        response.request_date = client_request.request_date
        response.request_id = client_request.request_id
        response.user = session_services.get_current_user()

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
            logging_services.exception(str(error))

        process_start_time = time()
        logging_services.info('request received with params: [{params}]'
                              .format(params=client_request.inputs))

        response = super(Application, self).full_dispatch_request()

        process_end_time = time()
        logging_services.info('request executed in [{time} ms].'
                              .format(time='{:0.3f}'
                                      .format((process_end_time - process_start_time) * 1000)))

        logging_services.debug('[{response}] returned with result: [{result}]'
                               .format(response=response,
                                       result=response.get_data(as_text=True)))

        return response
