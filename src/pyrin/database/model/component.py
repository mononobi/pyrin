# -*- coding: utf-8 -*-
"""
model component module.
"""

from pyrin.application.decorators import component
from pyrin.database.model import ModelPackage
from pyrin.database.model.manager import ModelManager
from pyrin.application.structs import Component


@component(ModelPackage.COMPONENT_NAME)
class ModelComponent(Component, ModelManager):
    """
    model component class.
    """
    pass
