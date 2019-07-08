# -*- coding: utf-8 -*-
"""
encryption package.
"""

from pyrin.packaging import Package


class EncryptionPackage(Package):
    """
    encryption package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.encryption.component'
