# -*- coding: utf-8 -*-
"""
api manager module.
"""

import pyrin.logging.services as logging_services

from pyrin.core.context import CoreObject
from pyrin.core.enumerations import ServerErrorResponseCodeEnum
from pyrin.utils import response as response_utils


class APIManager(CoreObject):
    """
    api manager class.
    """

    LOGGER = logging_services.get_logger('api')

    def handle_http_error(self, exception):
        """
        handles http exceptions.
        note that normally you should never call this method manually.

        :param HTTPException exception: exception instance.

        :rtype: CoreResponse
        """

        self.LOGGER.exception(str(exception))
        return response_utils.make_exception_response(exception)

    def handle_server_error(self, exception):
        """
        handles server internal core exceptions.
        note that normally you should never call this method manually.

        :param CoreException exception: core exception instance.

        :rtype: CoreResponse
        """

        self.LOGGER.exception(str(exception))
        return response_utils.make_exception_response(exception)

    def handle_server_unknown_error(self, exception):
        """
        handles unknown server internal exceptions.
        note that normally you should never call this method manually.

        :param Exception exception: exception instance.

        :rtype: CoreResponse
        """

        self.LOGGER.exception(str(exception))
        return response_utils.make_exception_response(exception,
                                                      code=ServerErrorResponseCodeEnum.
                                                      INTERNAL_SERVER_ERROR)
