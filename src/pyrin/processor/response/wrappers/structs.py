# -*- coding: utf-8 -*-
"""
response wrappers structs module.
"""

from pyrin.core.structs import Context


class ResponseContext(Context):
    """
    context class to hold response contextual data.
    """

    attribute_error_message = 'Property [{name}] not found in response context.'
