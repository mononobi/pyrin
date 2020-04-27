# -*- coding: utf-8 -*-
"""
mimetype component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.processor.mimetype import MIMETypePackage
from pyrin.processor.mimetype.manager import MIMETypeManager


@component(MIMETypePackage.COMPONENT_NAME)
class MIMETypeComponent(Component, MIMETypeManager):
    """
    mimetype component class.
    """
    pass
