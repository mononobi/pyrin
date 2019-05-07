# -*- coding: utf-8 -*-
"""
deserializer component module.
"""

from pyrin.converters.deserializer.manager import DeserializerManager
from pyrin.application.decorators import component
from pyrin.context import Component


@component()
class DeserializerComponent(Component, DeserializerManager):
    """
    deserializer component class.
    """

    COMPONENT_ID = __name__
