# -*- coding: utf-8 -*-
"""
hashing component module.
"""

from pyrin.application.decorators import component
from pyrin.security.hashing import HashingPackage
from pyrin.security.hashing.manager import HashingManager
from pyrin.application.structs import Component


@component(HashingPackage.COMPONENT_NAME)
class HashingComponent(Component, HashingManager):
    """
    hashing component class.
    """
    pass
