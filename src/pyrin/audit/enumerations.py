# -*- coding: utf-8 -*-
"""
audit enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class InspectionStatusEnum(CoreEnum):
    """
    inspection status enum.
    """

    OK = 'OK'
    FAILED = 'Failed'
