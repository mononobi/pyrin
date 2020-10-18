# -*- coding: utf-8 -*-
"""
api manager module.
"""

import pyrin.logging.services as logging_services
import pyrin.configuration.services as config_services
import pyrin.processor.response.services as response_services
import pyrin.security.session.services as session_services

from pyrin.api import APIPackage
from pyrin.api.exceptions import InvalidAPIHookTypeError
from pyrin.api.hooks import APIHookBase
from pyrin.core.mixin import HookMixin
from pyrin.core.structs import Manager
from pyrin.core.enumerations import ServerErrorResponseCodeEnum
from pyrin.core.globals import _


class APIManager(Manager, HookMixin):
    """
    api manager class.
    """

    package_class = APIPackage
    LOGGER = logging_services.get_logger('api')
    hook_type = APIHookBase
    invalid_hook_type_error = InvalidAPIHookTypeError

    def handle_http_error(self, exception):
        """
        handles http exceptions.

        note that normally you should never call this method manually.

        :param HTTPException exception: exception instance.

        :returns: tuple[dict | object, int, CoreHeaders]
        :rtype: tuple
        """

        self._log_exception(exception)
        return response_services.make_exception_response(exception,
                                                         request_id=self._get_request_id())

    def handle_server_business_error(self, exception):
        """
        handles server internal core business exceptions.

        note that normally you should never call this method manually.

        :param CoreBusinessException exception: core business exception instance.

        :returns: tuple[dict | object, int, CoreHeaders]
        :rtype: tuple
        """

        self._log_exception(exception)
        return response_services.make_exception_response(exception,
                                                         request_id=self._get_request_id(),
                                                         data=exception.data)

    def handle_server_error(self, exception):
        """
        handles server internal core exceptions.

        note that normally you should never call this method manually.
        in any environment which debug mode is False, the original error
        message will be replaced by a generic error message before being
        sent to client for security reasons.

        :param CoreException exception: core exception instance.

        :returns: tuple[dict | object, int, CoreHeaders]
        :rtype: tuple
        """

        self._log_exception(exception)
        if config_services.get_active('environment', 'debug') is True:
            return response_services.make_exception_response(exception,
                                                             request_id=self._get_request_id(),
                                                             data=exception.data)

        return response_services.make_error_response(self._get_generic_error_message(),
                                                     code=exception.code,
                                                     request_id=self._get_request_id())

    def handle_server_unknown_error(self, exception):
        """
        handles unknown server internal exceptions.

        note that normally you should never call this method manually.
        in any environment which debug mode is False, the original error
        message will be replaced by a generic error message before being
        sent to client for security reasons.

        :param Exception exception: exception instance.

        :returns: tuple[dict | object, int, CoreHeaders]
        :rtype: tuple
        """

        self._log_exception(exception)
        if config_services.get_active('environment', 'debug') is True:
            return response_services.make_exception_response(exception,
                                                             code=ServerErrorResponseCodeEnum.
                                                             INTERNAL_SERVER_ERROR,
                                                             request_id=self._get_request_id())

        return response_services.make_error_response(self._get_generic_error_message(),
                                                     code=ServerErrorResponseCodeEnum.
                                                     INTERNAL_SERVER_ERROR,
                                                     request_id=self._get_request_id())

    def _get_generic_error_message(self):
        """
        gets the generic error message to be sent to client.

        for any environment which debug mode is False.

        :rtype: str
        """

        return _('Application has been encountered an error. Please '
                 'contact the support team if problem persists.')

    def _get_request_id(self):
        """
        gets current request id.

        :rtype: uuid.UUID
        """

        return session_services.get_current_request_id()

    def _log_exception(self, exception):
        """
        logs the input exception.

        :param Exception exception: exception instance to be logged.
        """

        self.LOGGER.exception(str(exception))
        self._exception_occurred(exception)

    def _exception_occurred(self, error, **options):
        """
        this method will call `exception_occurred` method on all registered hooks.

        :param Exception error: exception instance that has been occurred.
        """

        for hook in self._get_hooks():
            hook.exception_occurred(error, **options)
