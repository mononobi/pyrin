# -*- coding: utf-8 -*-
"""
response wrappers structs module.
"""

from pyrin.core.exceptions import ContextAttributeError
from pyrin.core.structs import Context


class ResponseContext(Context):
    """
    context class to hold response contextual data.
    """

    def _raise_key_error(self, key):
        """
        raises an error for given key.

        :param object key: key object that caused the error.

        :raises ContextAttributeError: context attribute error.
        """

        raise ContextAttributeError('Property [{name}] not found in response context.'
                                    .format(name=key))
