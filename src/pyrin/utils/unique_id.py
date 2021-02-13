# -*- coding: utf-8 -*-
"""
utils unique_id module.
"""

import re
import uuid


# matches the uuid inside string.
# example: 2eaf043b-647a-45fb-b2a4-1d365a8eb548, 74314da0-6e34-11eb-8ce9-000000000000
# it matches all v1, v3, v4 and v5 uuids.
# matching is case-insensitive.
# the valid length is always 36.
UUID_REGEX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                        re.IGNORECASE)


def generate(**options):
    """
    generates a unique id based on input params.

    :keyword callable generator: uuid generator function.
                                 if not provided, defaults to uuid4.

    :rtype: uuid.UUID
    """

    generator = options.get('generator', uuid.uuid4)
    return generator()


def generate_uuid4():
    """
    generates a unique id using uuid4.

    :rtype: uuid.UUID
    """

    return generate(generator=uuid.uuid4)


def generate_uuid1():
    """
    generates a unique id using uuid1.

    :rtype: uuid.UUID
    """

    return generate(generator=uuid.uuid1)


def get_uuid(value):
    """
    gets the uuid object of given value.

    it raises an error if value is not a valid uuid string.

    :param str value: value to get uuid instance from it.

    :raises ValueError: value error.

    :rtype: uuid.UUID
    """

    return uuid.UUID(value)


def try_get_uuid(value):
    """
    gets the uuid object of given value.

    it returns None if value is not a valid uuid string.

    :param str value: value to get uuid instance from it.

    :rtype: uuid.UUID
    """

    try:
        return get_uuid(value)
    except Exception:
        return None


def try_get_uuid_or_value(value):
    """
    gets the uuid object of given value.

    it returns the same input if value is not a valid uuid string.

    :param str value: value to get uuid instance from it.

    :rtype: uuid.UUID | str
    """

    result = try_get_uuid(value)
    if result is None:
        return value

    return result
