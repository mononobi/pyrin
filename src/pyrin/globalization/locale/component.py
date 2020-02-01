# -*- coding: utf-8 -*-
"""
locale component module.
"""

from pyrin.application.decorators import component
from pyrin.globalization.locale import LocalePackage
from pyrin.globalization.locale.manager import LocaleManager
from pyrin.application.context import Component


@component(LocalePackage.COMPONENT_NAME)
class LocaleComponent(Component, LocaleManager):
    """
    locale component class.
    """
    pass
