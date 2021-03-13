# -*- coding: utf-8 -*-
"""
utils number module.
"""

from decimal import Decimal


def coerce_to_int(value):
    """
    gets the integer equivalent of given decimal or float value.

    if the real value does not have an int equivalent, it returns the same input.

    for example:

    coerce_to_int(1.2) -> 1.2
    coerce_to_int(1.0) -> 1
    coerce_to_int(1) -> 1
    coerce_to_int('1') -> '1'

    :param float | Decimal value: value to be coerced.

    :rtype: int | object
    """

    if not isinstance(value, (float, Decimal)):
        return value

    integer = int(value)
    if integer == value:
        return integer

    return value


def coerce_to_float(value):
    """
    gets the float equivalent of given decimal or integer value.

    if the real value does not have a float equivalent, it returns the same input.

    for example:

    coerce_to_float(1.2) -> 1.2
    coerce_to_float(1.0) -> 1.0
    coerce_to_float(1) -> 1.0
    coerce_to_float('1.2') -> '1.2'

    :param int | Decimal value: value to be coerced.

    :rtype: float | object
    """

    if not isinstance(value, (int, Decimal)) or isinstance(value, bool):
        return value

    return float(value)


def coerce_to_decimal(value):
    """
    gets the decimal equivalent of given float or integer value.

    if the real value does not have a decimal equivalent, it returns the same input.

    for example:

    coerce_to_decimal(1.2) -> 1.1999999
    coerce_to_decimal(1.0) -> 1.0
    coerce_to_decimal(1) -> 1.0
    coerce_to_decimal('1') -> '1'

    :param int | float value: value to be coerced.

    :rtype: Decimal | object
    """

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return value

    return Decimal(value)
