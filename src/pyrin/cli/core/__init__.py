# -*- coding: utf-8 -*-
"""
cli core package.

this package provides facilities to expose
`pyrin` global command after installing pyrin.
"""

from pyrin.packaging.base import Package


class CLICorePackage(Package):
    """
    cli core package class.
    """

    NAME = __name__
