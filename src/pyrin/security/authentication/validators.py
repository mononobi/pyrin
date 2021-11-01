# -*- coding: utf-8 -*-
"""
authentication validators module.
"""

from pyrin.validator.decorators import validator
from pyrin.validator.handlers.string import StringValidator


@validator('authentication', 'username')
@validator('authentication', 'password')
class CredentialValidator(StringValidator):
    """
    credential validator class.
    """

    default_nullable = False
    default_allow_blank = False
    default_allow_whitespace = False
