# -*- coding: utf-8 -*-
"""
validator auto package.
"""

from pyrin.packaging.base import Package


class ValidatorAutoPackage(Package):
    """
    validator auto package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'validator.auto.component'
    DEPENDS = ['pyrin.database.model']
