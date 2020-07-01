# -*- coding: utf-8 -*-
"""
request wrappers structs module.
"""

from pyrin.core.structs import Context


class RequestContext(Context):
    """
    context class to hold request contextual data.
    """

    attribute_error_message = 'Property [{name}] not found in request context.'
