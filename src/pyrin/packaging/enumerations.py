# -*- coding: utf-8 -*-
"""
packaging enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class PackageScopeEnum(CoreEnum):
    """
    package scope enum.
    """

    PYRIN = 0
    EXTENDED_APPLICATION = 1
    OTHER_APPLICATION = 2
    CUSTOM_APPLICATION = 3
    TEST = 4
    EXTENDED_UNIT_TEST = 5
    OTHER_UNIT_TEST = 6
    EXTENDED_INTEGRATION_TEST = 7
    OTHER_INTEGRATION_TEST = 8
    UNKNOWN = 100
