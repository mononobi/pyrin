# -*- coding: utf-8 -*-
"""
babel enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class BabelCLIHandlersEnum(CoreEnum):
    """
    babel cli handlers enum.
    """

    COMPILE = 'compile'
    EXTRACT = 'extract'
    INIT = 'init'
    UPDATE = 'update'
