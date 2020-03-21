# -*- coding: utf-8 -*-
"""
cli component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.cli import CLIPackage
from pyrin.cli.manager import CLIManager


@component(CLIPackage.COMPONENT_NAME)
class CLIComponent(Component, CLIManager):
    """
    cli component class.
    """
    pass
