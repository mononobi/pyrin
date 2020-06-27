# -*- coding: utf-8 -*-
"""
validator component module.
"""

from pyrin.application.decorators import component
from pyrin.validator import ValidatorPackage
from pyrin.validator.manager import ValidatorManager
from pyrin.application.structs import Component


@component(ValidatorPackage.COMPONENT_NAME)
class ValidatorComponent(Component, ValidatorManager):
    """
    validator component class.
    """
    pass
