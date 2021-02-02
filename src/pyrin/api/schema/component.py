# -*- coding: utf-8 -*-
"""
schema component module.
"""

from pyrin.api.schema import SchemaPackage
from pyrin.api.schema.manager import SchemaManager
from pyrin.application.decorators import component
from pyrin.application.structs import Component


@component(SchemaPackage.COMPONENT_NAME)
class SchemaComponent(Component, SchemaManager):
    """
    schema component class.
    """
    pass
