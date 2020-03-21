# -*- coding: utf-8 -*-
"""
logging component module.
"""

from pyrin.application.decorators import component
from pyrin.logging import LoggingPackage
from pyrin.logging.manager import LoggingManager
from pyrin.application.structs import Component


@component(LoggingPackage.COMPONENT_NAME)
class LoggingComponent(Component, LoggingManager):
    """
    logging component class.
    """
    pass
