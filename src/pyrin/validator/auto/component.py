# -*- coding: utf-8 -*-
"""
validator auto component module.
"""

from pyrin.application.decorators import component
from pyrin.validator.auto import ValidatorAutoPackage
from pyrin.validator.auto.manager import ValidatorAutoManager
from pyrin.application.structs import Component


@component(ValidatorAutoPackage.COMPONENT_NAME)
class ValidatorAutoComponent(Component, ValidatorAutoManager):
    """
    validator auto component class.
    """
    pass
