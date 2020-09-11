# -*- coding: utf-8 -*-
"""
logging hooks module.
"""

import pyrin.logging.services as logging_services

from pyrin.core.structs import Hook
from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase


class LoggingHookBase(Hook):
    """
    logging hook base class.

    all packages that need to be hooked into logging business must
    implement this class and register it in logging hooks.
    """

    def prepare_data(self, data, **options):
        """
        this method will be called when a log message interpolation is required.

        each subclass must return the modified or same input data.

        :param dict | object data: data that is passed to logging method.

        :returns: modified or same input data.
        :rtype: dict | object
        """

        return data

    def before_emit(self, message, data, level, **options):
        """
        this method will be called before a log is emitted.

        :param str message: the log message that must be emitted.
        :param dict | object data: data that is passed to logging method.
        :param int level: log level.
        """
        pass

    def after_emit(self, message, data, level, **options):
        """
        this method will be called after a log is emitted.

        :param str message: the log message that has been emitted.
        :param dict | object data: data that is passed to logging method.
        :param int level: log level.
        """
        pass


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def after_packages_loaded(self):
        """
        this method will be called after all application packages have been loaded.
        """

        # we must wrap all available loggers into an adapter
        # to inject request info into every log record.
        # it does not affect sqlalchemy logs.
        logging_services.wrap_all_loggers()
