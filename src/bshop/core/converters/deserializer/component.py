# -*- coding: utf-8 -*-
"""
deserializer component module.
"""

from bshop.core.converters.deserializer.manager import DeserializerManager
from bshop.core.application.decorators import component
from bshop.core.context import Component


@component()
class DeserializerComponent(Component, DeserializerManager):
    """
    deserializer component class.
    """

    COMPONENT_ID = __name__
