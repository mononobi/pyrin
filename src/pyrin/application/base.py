# -*- coding: utf-8 -*-
"""
application base module.
"""

import signal
import sys

from flask import Flask, request
from flask.app import setupmethod

import pyrin.packaging.services as packaging_services

from pyrin import settings
from pyrin import _set_app
from pyrin.api.router.handlers.protected import SimpleProtectedRoute
from pyrin.converters.json.decoder import CoreJSONDecoder
from pyrin.converters.json.encoder import CoreJSONEncoder
from pyrin.packaging.component import PackagingComponent
from pyrin.application.context import CoreResponse, CoreRequest
from pyrin.context import Context, Component, ContextAttributeError
from pyrin.exceptions import CoreValueError, CoreTypeError, CoreKeyError
from pyrin.settings import DEFAULT_COMPONENT_KEY
from pyrin.utils.custom_print import print_warning, print_error


class ApplicationContext(Context):
    """
    context class to hold application contextual data.
    """
    pass


class ComponentAttributeError(ContextAttributeError):
    """
    component attribute error.
    """
    pass


class ApplicationComponent(ApplicationContext):
    """
    context class to hold application components.
    """

    def __getattr__(self, name):
        if name in self:
            return self.get(name)

        raise ComponentAttributeError('Component [{name}] is not available '
                                      'in application components.'.format(name=name))


class Application(Flask):
    """
    application class.
    server must initialize an instance of this class at startup.
    """

    # we set `url_rule_class = SimpleProtectedRoute` to force top
    # level application to register it's own desired route factory.
    url_rule_class = SimpleProtectedRoute
    response_class = CoreResponse
    request_class = CoreRequest
    json_decoder = CoreJSONDecoder
    json_encoder = CoreJSONEncoder

    def __init__(self, import_name, **options):
        """
        initializes an instance of Application.

        :param str import_name: name of the main application package.

        :keyword str static_url_path: can be used to specify a different path for the
                                      static files on the web. defaults to the name
                                      of the `static_folder` folder.

        :keyword str static_folder: the folder with static files that should be served
                                    at `static_url_path`. defaults to the `static`
                                    folder in the root path of the application.

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

        :keyword str root_path: Flask by default will automatically calculate the path
                                to the root of the application. in certain situations
                                this cannot be achieved (for instance if the package
                                is a Python 3 namespace package) and needs to be
                                manually defined.
        """

        super(Application, self).__init__(import_name, **options)

        self._context = ApplicationContext()
        self._components = ApplicationComponent()

        # we should register packaging component manually because it is the base package
        # and could not be loaded automatically due to circular references through imports.
        self.register_component(PackagingComponent())

        # setting the application instance in global 'pyrin' level variable.
        _set_app(self)

    def add_context(self, key, value):
        """
        adds the given key and it's value into the application context.

        :param str key: related key for storing application context.
        :param object value: related value for storing in application context.
        """

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

        :raises CoreTypeError: core type error.
        :raises CoreValueError: core value error.
        :raises CoreKeyError: core key error.
        """

        if not isinstance(component, Component):
            raise CoreTypeError('Input parameter [{component}] is not '
                                'an instance of Component.'.format(component=str(component)))

        if not isinstance(component.COMPONENT_ID, tuple) or \
                len(component.COMPONENT_ID[0].strip()) == 0:
            raise CoreValueError('Component [{component}] has '
                                 'not a valid component id.'.format(component=str(component)))

        # checking whether is there any registered component with the same id.
        if component.COMPONENT_ID in self._components.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise CoreKeyError('There is another registered component with id [{id}] '
                                   'but "replace" option is not set, so component '
                                   '[{instance}] could not be registered.'
                                   .format(id=component.COMPONENT_ID,
                                           instance=str(component)))

            old_instance = self._components[component.COMPONENT_ID]
            print_warning('Component [{old_instance}] is going to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(component)))

        self._components[component.COMPONENT_ID] = component

    def get_component(self, component_id, **options):
        """
        gets the specified application component.

        :param str component_id: component unique id.

        :keyword object custom_key: custom key of component to get.

        :rtype: Component
        """

        # checking whether is there any custom implementation for this component.
        key = options.get('custom_key', DEFAULT_COMPONENT_KEY)
        if (component_id[0], key) in self._components.keys():
            return self._components[(component_id[0], key)]

        # getting default component.
        return self._components[component_id]

    def _load(self, **options):
        """
        loads application configs and components.
        """

        self._configure(**options)
        packaging_services.load_components(**options)

    def _configure(self, **options):
        """
        configures application.
        """

        self.config.from_object(settings)

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
        super(Application, self).run(host, port, debug, load_dotenv, **options)

    def dispatch_request(self):
        """
        does the request dispatching. matches the URL and returns the
        return value of the view or error handlers. this does not have to
        be a response object. in order to convert the return value to a
        proper response object, call `make_response` function.
        """

        # we have to override whole `dispatch_request` method to be able to customize it,
        # because of the poor design of flask that everything is embedded inside
        # the `dispatch_request` method.
        with request:
            if request.routing_exception is not None:
                self.raise_routing_exception(request)

            route = request.url_rule
            # if we provide automatic options for this URL and the
            # request came with the OPTIONS method, reply automatically.
            if getattr(route, 'provide_automatic_options', False) \
               and request.method == 'OPTIONS':
                return self.make_default_options_response()

            # otherwise dispatch the handler for that route.
            return route.dispatch(request)

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
                                               added automatically. this can also be controlled
                                               by setting the `view_func.provide_automatic_options = False`
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

        :raises CoreKeyError: core key error.
        """

        methods = options.get('methods', ())
        if not isinstance(methods, (tuple, list, set)):
            options.update(methods=(methods,))

        replace = options.get('replace', False)

        # setting endpoint to url rule instead of view function name,
        # to be able to have the same function name on different url rules.
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

                print_warning('Registered route for url [{url}] is going to be replaced by a new route.'
                              .format(url=rule))
            else:
                raise CoreKeyError('There is another registered route with the same url [{url}], '
                                   'but "replace" option is not set, so the new route could not be registered.'
                                   .format(url=rule))

        # we have to put `view_function=view_func` into options to be able to deliver it to
        # route initialization in the super method. that's because of poor design of flask
        # that does not forward all params to inner method calls. and this is the less ugly way
        # in comparison with overriding the whole `add_url_rule` function.
        options.update(view_function=view_func)

        super(Application, self).add_url_rule(rule, endpoint, view_func,
                                              provide_automatic_options, **options)

    def terminate(self, **options):
        """
        terminates the application.
        """

        print_error('Terminating application [{name}].'.format(name=self.name))

        # forcing termination after 10 seconds.
        signal.alarm(10)
        sys.exit(0)

    def register_route_factory(self, factory):
        """
        registers a route factory as application url rule class.

        :param callable factory: route factory.
                                 it could be a class or a factory method.

        :raises CoreTypeError: core type error.
        """

        if not callable(factory):
            raise CoreTypeError('Input parameter [{factory}] is not callable.'
                                .format(factory=str(factory)))

        Application.url_rule_class = factory
