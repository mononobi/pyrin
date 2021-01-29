# -*- coding: utf-8 -*-
"""
cors component module.
"""

from pyrin.processor.cors import CORSPackage
from pyrin.processor.cors.manager import CORSManager
from pyrin.application.decorators import component
from pyrin.application.structs import Component


@component(CORSPackage.COMPONENT_NAME)
class CORSComponent(Component, CORSManager):
    """
    cors component class.
    """
    pass
