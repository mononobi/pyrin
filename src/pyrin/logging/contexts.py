# -*- coding: utf-8 -*-
"""
logging contexts module.
"""

import pyrin.logging.services as logging_services

from pyrin.core.contexts import ContextManagerBase


class suppress(ContextManagerBase):
    """
    context manager to suppress any exceptions and logs them.

    for example:

    def service1():
        with suppress():
            raise Exception('Error Occurred')

    def service2():
        with suppress(ValueError, TypeError, log=False):
            raise ValueError('Error Occurred')
    """

    def __init__(self, *errors, **options):
        """
        initializes an instance of suppress.

        :param type[Exception] errors: exception types to be suppressed.
                                       if not provided, all exceptions will
                                       be suppressed.

        :keyword bool log: log suppressed exceptions.
                           defaults to True if not provided.
        """

        if errors is None or len(errors) <= 0:
            errors = (Exception,)

        self._errors = errors
        self._log = options.get('log', True)

        super().__init__()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        does the finalizing to suppress and log and required errors.

        :param type[Exception] exc_type: the exception type that has been
                                         occurred during current context.

        :param Exception exc_value: exception instance that has been
                                    occurred during current context.

        :param traceback traceback: traceback of occurred exception.
        """

        suppressed = isinstance(exc_value, self._errors)
        if suppressed is True and self._log is True:
            logging_services.exception(str(exc_value))

        return suppressed
