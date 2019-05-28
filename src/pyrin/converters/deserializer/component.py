# -*- coding: utf-8 -*-
"""
deserializer component module.
"""

from pyrin.converters.deserializer import DeserializerPackage
from pyrin.converters.deserializer.manager import DeserializerManager
from pyrin.application.decorators import component
from pyrin.core.context import Component


@component(DeserializerPackage.COMPONENT_NAME)
class DeserializerComponent(Component, DeserializerManager):
    """
    deserializer component class.
    """
