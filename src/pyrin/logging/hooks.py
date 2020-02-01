# -*- coding: utf-8 -*-
"""
logging hooks module.
"""

import pyrin.logging.services as logging_services

from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def __init__(self):
        """
        initializes an instance of PackagingHook.
        """

        super().__init__()

    def after_packages_loaded(self):
        """
        this method will be called after all application packages has been loaded.
        """

        # we must wrap all available loggers into an adapter
        # to inject request info into every log record.
        # it does not affect sqlalchemy logs.
        logging_services.wrap_all_loggers()
