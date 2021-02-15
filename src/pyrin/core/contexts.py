# -*- coding: utf-8 -*-
"""
core contexts module.
"""

from contextlib import AbstractContextManager


class ContextManagerBase(AbstractContextManager):
    """
    context manager base class.

    this class should be used as the base for all application context managers.
    """

    def _should_be_raised(self, internal_error, context_exception_type):
        """
        gets a value indicating that given internal error should be raised.

        considering the exception type that has been occurred inside context.

        :param Exception internal_error: exception instance that has been occurred
                                         inside the context manager itself.

        :param type[Exception] context_exception_type: the exception type that has been
                                                       occurred inside the context but
                                                       not in context manager itself.

        :rtype: bool
        """

        return context_exception_type is None or \
            type(internal_error) is not context_exception_type
