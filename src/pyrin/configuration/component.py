# -*- coding: utf-8 -*-
"""
configuration component module.
"""

from pyrin.application.decorators import component
from pyrin.configuration.manager import ConfigurationManager
from pyrin.context import Component
from pyrin.settings.static import DEFAULT_COMPONENT_KEY


@component()
class ConfigurationComponent(Component, ConfigurationManager):
    """
    configuration component class.
    """

    COMPONENT_ID = (__name__, DEFAULT_COMPONENT_KEY)
