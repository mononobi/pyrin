# -*- coding: utf-8 -*-
"""
swagger component module.
"""

from pyrin.api.swagger import SwaggerPackage
from pyrin.api.swagger.manager import SwaggerManager
from pyrin.application.decorators import component
from pyrin.application.structs import Component


@component(SwaggerPackage.COMPONENT_NAME)
class SwaggerComponent(Component, SwaggerManager):
    """
    swagger component class.
    """
    pass
