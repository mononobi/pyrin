# -*- coding: utf-8 -*-
"""
serializer component module.
"""

from pyrin.converters.serializer import SerializerPackage
from pyrin.converters.serializer.manager import SerializerManager
from pyrin.application.decorators import component
from pyrin.application.structs import Component


@component(SerializerPackage.COMPONENT_NAME)
class SerializerComponent(Component, SerializerManager):
    """
    serializer component class.
    """
    pass
