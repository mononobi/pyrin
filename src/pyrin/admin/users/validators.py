# -*- coding: utf-8 -*-
"""
admin users validators module.
"""

from pyrin.admin.enumerations import FormFieldTypeEnum
from pyrin.admin.users.models import AdminUserEntity
from pyrin.validator.decorators import validator
from pyrin.validator.handlers.string import StringValidator


@validator(AdminUserEntity, AdminUserEntity.password_hash, name='password')
@validator(AdminUserEntity, AdminUserEntity.password_hash, name='confirm_password')
class PasswordValidator(StringValidator):
    """
    password validator class.
    """

    default_minimum_length = 8
    default_maximum_length = 50
    default_form_field_type = FormFieldTypeEnum.PASSWORD
