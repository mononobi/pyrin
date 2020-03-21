# -*- coding: utf-8 -*-
"""
api component module.
"""

from pyrin.application.decorators import component
from pyrin.api import APIPackage
from pyrin.api.manager import APIManager
from pyrin.application.structs import Component


@component(APIPackage.COMPONENT_NAME)
class APIComponent(Component, APIManager):
    """
    api component class.
    """
    pass
