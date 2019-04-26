# -*- coding: utf-8 -*-
"""
Deserializers services module.
"""

from bshop.core.api.deserializers.component import DeserializersComponent
from bshop.core.application.services import get_component


def deserialize(value, **options):
    """
    Deserializes the given value.
    Returns None if deserialization fails.

    :param str value: value to be deserialized.

    :rtype: object
    """

    return get_component(DeserializersComponent.COMPONENT_ID).deserialize(value, **options)
