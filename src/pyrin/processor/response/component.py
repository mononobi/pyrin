# -*- coding: utf-8 -*-
"""
response component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.processor.response import ResponsePackage
from pyrin.processor.response.manager import ResponseManager


@component(ResponsePackage.COMPONENT_NAME)
class ResponseComponent(Component, ResponseManager):
    """
    response component class.
    """
    pass
