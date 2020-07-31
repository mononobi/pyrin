# -*- coding: utf-8 -*-
"""
logging masking services module.
"""

from pyrin.application.services import get_component
from pyrin.logging.masking import LoggingMaskingPackage


def should_mask(key):
    """
    gets a value indicating that given key should be masked in a dict.

    :param str key: dict key to be checked.

    :rtype: bool
    """

    return get_component(LoggingMaskingPackage.COMPONENT_NAME).should_mask(key)


def mask(data, **options):
    """
    masks the given data if required.

    if data is not a dict, no changes will be made.

    :param dict | object data: data to be masked.

    :returns: a masked dict or original input data.
    :rtype: MaskedDict | object
    """

    return get_component(LoggingMaskingPackage.COMPONENT_NAME).mask(data, **options)
