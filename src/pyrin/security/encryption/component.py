# -*- coding: utf-8 -*-
"""
encryption component module.
"""

from pyrin.application.decorators import component
from pyrin.security.encryption import EncryptionPackage
from pyrin.security.encryption.manager import EncryptionManager
from pyrin.application.structs import Component


@component(EncryptionPackage.COMPONENT_NAME)
class EncryptionComponent(Component, EncryptionManager):
    """
    encryption component class.
    """
    pass
