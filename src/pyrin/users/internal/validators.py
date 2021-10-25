# -*- coding: utf-8 -*-
"""
users internal validators module.
"""

from pyrin.admin.enumerations import FormFieldTypeEnum
from pyrin.users.internal.models import InternalUserEntity
from pyrin.validator.decorators import validator
from pyrin.validator.handlers.string import StringValidator


@validator(InternalUserEntity, InternalUserEntity.password_hash, name='password')
@validator(InternalUserEntity, InternalUserEntity.password_hash, name='confirm_password')
class PasswordValidator(StringValidator):
    """
    password validator class.
    """

    default_minimum_length = 8
    default_maximum_length = 50
    default_form_field_type = FormFieldTypeEnum.PASSWORD
