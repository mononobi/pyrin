# -*- coding: utf-8 -*-
"""
Application base module.
"""

from flask import Flask
# from flask.globals import _request_ctx_stack

import bshop.core.packaging.services as packaging_services

from bshop.core.api.context import ResponseBase, RequestBase
from bshop.core.context import Context, Component
from bshop import settings
from bshop.core.exceptions import CoreTypeError


class ApplicationContext(Context):
    """
    Context class to hold application contextual data.
    """
    pass


class ApplicationComponent(ApplicationContext):
    """
    Context class to hold application components.
    """
    pass


class Application(Flask):
    """
    Application class.
    Server must initialize an instance of this class at startup.
    """

    response_class = ResponseBase
    request_class = RequestBase

    def __init__(self, import_name, **options):
        """
        Initializes an instance of Application.

        :param str import_name: name of the main application package.

        :keyword str static_url_path: can be used to specify a different path for the
                                      static files on the web. Defaults to the name
                                      of the `static_folder` folder.
        :keyword str static_folder: the folder with static files that should be served
                                    at `static_url_path`. Defaults to the ``'static'``
                                    folder in the root path of the application.
        :keyword str static_host: the host to use when adding the static route.
                                  Defaults to None. Required when using ``host_matching=True``
                                  with a ``static_folder`` configured.
        :keyword bool host_matching: set ``url_map.host_matching`` attribute.
                                     Defaults to False.
        :keyword str subdomain_matching: consider the subdomain relative to
                                         :data:`SERVER_NAME` when matching routes. Defaults to False.
        :keyword str template_folder: the folder that contains the templates that should
                                      be used by the application. Defaults to
                                      ``'templates'`` folder in the root path of the application.
        :keyword str instance_path: An alternative instance path for the application.
                                    By default the folder ``'instance'`` next to the
                                    package or module is assumed to be the instance path.
        :keyword bool instance_relative_config: if set to ``True`` relative filenames
                                                for loading the config are assumed to
                                                be relative to the instance path instead
                                                of the application root.
        :keyword str root_path: Flask by default will automatically calculate the path
                                to the root of the application. In certain situations
                                this cannot be achieved (for instance if the package
                                is a Python 3 namespace package) and needs to be
                                manually defined.
        """

        super(Application, self).__init__(import_name, **options)
        self._context = ApplicationContext()
        self._components = ApplicationComponent()

    def add_context(self, key, value):
        """
        Adds the given key and it's value into the application context.

        :param str key: related key for storing application context.
        :param object value: related value for storing in application context.
        """

        self._context[key] = value

    def get_context(self, key):
        """
        Gets the application context value that belongs to given key.

        :param str key: key for requested application context.

        :rtype: object
        """

        return self._context[key]

    def register_component(self, component, **options):
        """
        Registers given application component.

        :param Component component: component instance.

        :raises CoreTypeError: core type error.
        """

        if not isinstance(component, Component):
            raise CoreTypeError('Input parameter [{component}] is not '
                                'an instance of Component.'.format(component=str(component)))

        self._components[component.COMPONENT_ID] = component

    def get_component(self, component_id, **options):
        """
        Gets the specified application component.

        :param str component_id: component unique id.

        :rtype: Component
        """

        return self._components[component_id]

    def _load(self, **options):
        """
        Loads application configs and components.
        """

        self._configure(**options)
        packaging_services.load_components(**options)

    def _configure(self, **options):
        """
        Configures application.
        """

        self.config.from_object(settings)

    def run(self, host=None, port=None, debug=None,
            load_dotenv=True, **options):
        """
        Runs the Application instance.

        :param str host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
                         have the server available externally as well. Defaults to
                         ``'127.0.0.1'`` or the host in the ``SERVER_NAME``
                         config variable if present.
        :param int port: the port of the webserver. Defaults to ``5000`` or the
                         port defined in the ``SERVER_NAME`` config variable if present.
        :param bool debug: if given, enable or disable debug mode.
        :param bool load_dotenv: Load the nearest :file:`.env` and :file:`.flaskenv`
                                 files to set environment variables. Will also change the working
                                 directory to the directory containing the first file found.
        """

        self._load()
        super(Application, self).run(host, port, debug, load_dotenv, **options)

    # def dispatch_request(self):
    #     """
    #     Does the request dispatching. Matches the URL and returns the
    #     return value of the view or error handler. This does not have to
    #     be a response object. In order to convert the return value to a
    #     proper response object, call :func:`make_response`.
    #
    #     This method is overridden to make it possible to pass all request parameters
    #     to the underlying view method.
    #     """
    #
    #     request = _request_ctx_stack.top.request
    #
    #     params = DynamicObject(**(request.view_args or {}),
    #                            **(request.get_json(force=True, silent=True) or {}),
    #                            query_params=request.args,
    #                            files=request.files)
    #
    #     request.view_args = params
    #
    #     return super(Application, self).dispatch_request()
