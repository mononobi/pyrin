# -*- coding: utf-8 -*-
"""
application base module.
"""

from flask import Flask

import bshop.core.packaging.services as packaging_services

from bshop.core.packaging.component import PackagingComponent
from bshop import settings
from bshop.core import _set_app
from bshop.core.api.context import ResponseBase, RequestBase
from bshop.core.context import Context, Component, ContextAttributeError
from bshop.core.exceptions import CoreValueError, CoreTypeError


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

    response_class = ResponseBase
    request_class = RequestBase

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
        # and could not be loaded automatically due to references through imports.
        self.register_component(PackagingComponent())

        # setting the application instance in global 'bshop.core' level variable.
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

    def register_component(self, component, **options):
        """
        registers given application component.

        :param Component component: component instance.

        :raises CoreTypeError: core type error.
        """

        if not isinstance(component, Component):
            raise CoreTypeError('Input parameter [{component}] is not '
                                'an instance of Component.'.format(component=str(component)))

        if component.COMPONENT_ID is None or \
                len(component.COMPONENT_ID.strip()) == 0:
            raise CoreValueError('Component [{component}] has '
                                 'not a valid component id.'.format(component=str(component)))

        self._components[component.COMPONENT_ID] = component

    def get_component(self, component_id, **options):
        """
        gets the specified application component.

        :param str component_id: component unique id.

        :rtype: Component
        """

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

        this method is overridden to make it possible to pass all request parameters
        to the underlying view method.
        """

        return super(Application, self).dispatch_request()
