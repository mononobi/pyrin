# -*- coding: utf-8 -*-
"""
pyrin tests main package.
"""

import os
import signal

from pyrin.utils.custom_print import print_error
from pyrin.application.base import Application


class PyrinTestApplication(Application):
    """
    pyrin test application class.
    test server should create an instance of this class on startup.
    """

    def __init__(self, **options):
        """
        initializes an instance of PyrinTestApplication.

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

        :keyword str root_path: flask by default will automatically calculate the path
                                to the root of the application. in certain situations
                                this cannot be achieved (for instance if the package
                                is a python 3 namespace package) and needs to be
                                manually defined.

        :keyword bool migration: specifies that the application has been run to
                                 do a migration. some application hooks will not
                                 get fired when the app runs in migration mode.
                                 defaults to False, if not provided.
        """

        super().__init__(self.get_application_name(), **options)

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

        :param int signal_number: signal number.
        :param Union[int, FrameType] frame: interrupted stack frame.
        """

        print_error('A TERMINATION SIGNAL CAUGHT! signal [{signal_number}] '
                    'is going to terminate the application [{name}].'
                    .format(signal_number=signal_number, name=self.name))

        # terminating the application with status=1 to notice a failure.
        self.terminate(status=1)

    def _resolve_application_main_package_path(self, **options):
        """
        resolves the application main package path.
        each derived class from Application, must override this method,
        and resolve it's own main package path.

        :rtype: str
        """

        return os.path.abspath(__path__[0])

    @classmethod
    def get_application_name(cls):
        """
        gets the application name.

        :rtype: str
        """

        return __name__.split('.')[0]
