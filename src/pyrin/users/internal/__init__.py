# -*- coding: utf-8 -*-
"""
users internal package.
"""

from pyrin.packaging.base import Package


class InternalUsersPackage(Package):
    """
    internal users package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'users.internal.component'
    DEPENDS = ['pyrin.admin',
               'pyrin.validator',
               'pyrin.database.model']
