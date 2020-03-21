# -*- coding: utf-8 -*-
"""
configuration component module.
"""

from pyrin.application.decorators import component
from pyrin.configuration import ConfigurationPackage
from pyrin.configuration.manager import ConfigurationManager
from pyrin.application.structs import Component


@component(ConfigurationPackage.COMPONENT_NAME)
class ConfigurationComponent(Component, ConfigurationManager):
    """
    configuration component class.
    """
    pass
