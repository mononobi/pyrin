# -*- coding: utf-8 -*-
"""
logging masking component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.logging.masking import LoggingMaskingPackage
from pyrin.logging.masking.manager import LoggingMaskingManager


@component(LoggingMaskingPackage.COMPONENT_NAME)
class LoggingMaskingComponent(Component, LoggingMaskingManager):
    """
    logging masking component class.
    """
    pass
