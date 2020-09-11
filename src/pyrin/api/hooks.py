# -*- coding: utf-8 -*-
"""
api hooks module.
"""

from pyrin.core.structs import Hook


class APIHookBase(Hook):
    """
    api hook base class.

    all packages that need to be hooked into api business must
    implement this class and register it in api hooks.
    """

    def exception_occurred(self, error, **options):
        """
        this method will be called when an exception is occurred.

        :param Exception error: exception instance that has been occurred.
        """
        pass
