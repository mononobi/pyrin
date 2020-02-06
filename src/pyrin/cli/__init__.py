# -*- coding: utf-8 -*-
"""
cli package.
this package provides facilities to execute commands in shell.
"""

from pyrin.packaging.context import Package


class CLIPackage(Package):
    """
    cli package class.
    """

    NAME = __name__
    DEPENDS = []
