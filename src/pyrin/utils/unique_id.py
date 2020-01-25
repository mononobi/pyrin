# -*- coding: utf-8 -*-
"""
utils unique_id module.
"""

import uuid


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
