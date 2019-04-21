# -*- coding: utf-8 -*-
"""
Application base module.
"""

from flask import Flask

from bshop.core.api_context import ResponseBase, RequestBase


class Application(Flask):
    """
    Application class.
    Server must initialize an instance of this class at startup.
    """

    response_class = ResponseBase
    request_class = RequestBase

    def __init__(self, import_name, **kwargs):
        """
        Initializes an instance of Application.

        :param str import_name: the name of the application package.

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

        super(Application, self).__init__(import_name, **kwargs)

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
        :param dict options: the options to be forwarded to the underlying Werkzeug server.
        """

        super(Application, self).run(host, port, debug, load_dotenv, **options)
