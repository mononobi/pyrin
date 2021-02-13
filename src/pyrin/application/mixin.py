# -*- coding: utf-8 -*-
"""
application mixin module.
"""

import sys
import signal

from abc import abstractmethod

import pyrin.logging.services as logging_services

from pyrin.core.structs import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class SignalMixin(CoreObject):
    """
    signal mixin class.

    every class which needs to handle signals must inherit from this.
    note that not all operating systems support signals, so this will work on some of them.
    """

    def __init__(self, **options):
        """
        initializes an instance of SignalMixin.
        """

        super().__init__()

        # handling all signals that their default action is `terminate`,
        # to log if something goes wrong.
        try:
            signal.signal(signal.SIGABRT, self._log_signal)
            signal.signal(signal.SIGBUS, self._log_signal)
            signal.signal(signal.SIGFPE, self._log_signal)
            signal.signal(signal.SIGHUP, self._log_signal)
            signal.signal(signal.SIGILL, self._log_signal)
            signal.signal(signal.SIGPIPE, self._log_signal)
            signal.signal(signal.SIGPOLL, self._log_signal)
            signal.signal(signal.SIGPROF, self._log_signal)
            signal.signal(signal.SIGRTMIN, self._log_signal)
            signal.signal(signal.SIGRTMAX, self._log_signal)
            signal.signal(signal.SIGQUIT, self._log_signal)
            signal.signal(signal.SIGSEGV, self._log_signal)
            signal.signal(signal.SIGSYS, self._log_signal)
            signal.signal(signal.SIGTRAP, self._log_signal)
            signal.signal(signal.SIGXCPU, self._log_signal)
            signal.signal(signal.SIGXFSZ, self._log_signal)
        except Exception:
            # ignore on systems that do not support signals.
            pass

    def _log_signal(self, signal_number, frame):
        """
        logs the caught termination signal and terminates the application.

        :param int signal_number: signal number that caused termination.
        :param int | FrameType frame: interrupted stack frame.
        """

        message = 'A TERMINATION SIGNAL CAUGHT! signal [{signal_number}] ' \
                  'is going to terminate the application [{name}].' \
            .format(signal_number=signal_number,
                    name=self.get_application_name())

        logging_services.error(message)

        # terminating the application with 'status = 1' to notice a failure.
        self._terminate(signal_number, status=1)

    def _terminate(self, signal_number, **options):
        """
        terminates the application.

        this method should not be called directly.
        it is defined for cases that application has to
        be terminated for some unexpected reasons.

        :param int signal_number: signal number that caused termination.

        :keyword int status: status code to use for application exit.
                             if not provided, status=0 will be used.
        """

        message = 'Terminating application [{name}].'.format(
            name=self.get_application_name())

        logging_services.error(message)

        # forcing termination after 60 seconds if it was not done.
        signal.alarm(60)

        self._prepare_termination(signal_number)
        sys.exit(options.get('status', 0))

    @abstractmethod
    def get_application_name(self):
        """
        gets the application name.

        this method must be implemented in subclasses.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _prepare_termination(self, signal_number):
        """
        prepares for termination.

        this method is intended to be overridden in subclasses.

        :param int signal_number: signal number that caused termination.
        """
        pass
