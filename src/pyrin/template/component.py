# -*- coding: utf-8 -*-
"""
template component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.template import TemplatePackage
from pyrin.template.manager import TemplateManager


@component(TemplatePackage.COMPONENT_NAME)
class TemplateComponent(Component, TemplateManager):
    """
    template component class.
    """
    pass
