# -*- coding: utf-8 -*-
"""
cors hooks module.
"""

import pyrin.processor.cors.services as cors_services

from pyrin.application.decorators import application_hook
from pyrin.application.hooks import ApplicationHookBase


@application_hook()
class ApplicationHook(ApplicationHookBase):
    """
    application hook class.
    """

    def provide_response_headers(self, headers, endpoint,
                                 status_code, method, **options):
        """
        this method will be called whenever a response is going to be returned from server.

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

        cors_headers = cors_services.get_current_cors_headers()
        if cors_headers is not None:
            headers.extend(cors_headers)
