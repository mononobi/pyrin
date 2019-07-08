# -*- coding: utf-8 -*-
"""
localization component module.
"""

from pyrin.application.decorators import component
from pyrin.localization import LocalizationPackage
from pyrin.localization.manager import LocalizationManager
from pyrin.application.context import Component


@component(LocalizationPackage.COMPONENT_NAME)
class LocalizationComponent(Component, LocalizationManager):
    """
    localization component class.
    """
