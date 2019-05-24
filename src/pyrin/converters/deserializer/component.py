# -*- coding: utf-8 -*-
"""
deserializer component module.
"""

from pyrin.converters.deserializer.manager import DeserializerManager
from pyrin.application.decorators import component
from pyrin.core.context import Component
from pyrin.settings.static import DEFAULT_COMPONENT_KEY


@component()
class DeserializerComponent(Component, DeserializerManager):
    """
    deserializer component class.
    """

    COMPONENT_ID = (__name__, DEFAULT_COMPONENT_KEY)
