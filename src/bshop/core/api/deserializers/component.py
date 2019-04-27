# -*- coding: utf-8 -*-
"""
Deserializers component module.
"""

from bshop.core.api.deserializers.manager import DeserializersManager
from bshop.core.application.decorators import register_component
from bshop.core.context import Component


@register_component()
class DeserializersComponent(Component, DeserializersManager):
    """
    Deserializers component class.
    """

    COMPONENT_ID = __name__
