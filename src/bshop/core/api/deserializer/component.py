# -*- coding: utf-8 -*-
"""
deserializer component module.
"""

from bshop.core.api.deserializer.manager import DeserializerManager
from bshop.core.application.decorators import register_component
from bshop.core.context import Component


@register_component()
class DeserializerComponent(Component, DeserializerManager):
    """
    deserializer component class.
    """

    COMPONENT_ID = __name__
