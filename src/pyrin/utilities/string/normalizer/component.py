# -*- coding: utf-8 -*-
"""
string normalizer component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.utilities.string.normalizer import StringNormalizerPackage
from pyrin.utilities.string.normalizer.manager import StringNormalizerManager


@component(StringNormalizerPackage.COMPONENT_NAME)
class StringNormalizerComponent(Component, StringNormalizerManager):
    """
    string normalizer component class.
    """
    pass
