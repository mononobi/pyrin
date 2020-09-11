# -*- coding: utf-8 -*-
"""
sentry component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.logging.sentry import SentryPackage
from pyrin.logging.sentry.manager import SentryManager


@component(SentryPackage.COMPONENT_NAME)
class SentryComponent(Component, SentryManager):
    """
    sentry component class.
    """
    pass
