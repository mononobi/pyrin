# -*- coding: utf-8 -*-
"""
response status component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.processor.response.status import ResponseStatusPackage
from pyrin.processor.response.status.manager import ResponseStatusManager


@component(ResponseStatusPackage.COMPONENT_NAME)
class ResponseStatusComponent(Component, ResponseStatusManager):
    """
    response status component class.
    """
    pass
