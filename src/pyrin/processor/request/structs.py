# -*- coding: utf-8 -*-
"""
request structs module.
"""

from pyrin.core.exceptions import ContextAttributeError
from pyrin.core.structs import Context


class RequestContext(Context):
    """
    context class to hold request contextual data.
    """

    def _raise_key_error(self, key):
        """
        raises an error for given key.

        :param object key: key object that caused the error.

        :raises ContextAttributeError: context attribute error.
        """

        raise ContextAttributeError('Property [{name}] not found in request context.'
                                    .format(name=key))
