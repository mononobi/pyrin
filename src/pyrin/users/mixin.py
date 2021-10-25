# -*- coding: utf-8 -*-
"""
users mixin module.
"""

from sqlalchemy import Unicode
from sqlalchemy.ext.hybrid import hybrid_property

from pyrin.core.globals import _
from pyrin.core.enumerations import CoreEnum, EnumMember
from pyrin.database.orm.sql.schema.columns import AutoPKColumn, StringColumn, \
    SmallIntegerColumn, BooleanColumn, TimeStampColumn, HiddenColumn


class UserPKMixin:
    """
    user pk mixin class.
    """

    id = AutoPKColumn(name='id')


class UserCredentialMixin:
    """
    user credential mixin class.
    """

    username = StringColumn(name='username', min_length=1, max_length=30,
                            unique=True, index=True, nullable=False)
    password_hash = HiddenColumn(name='password_hash', type_=Unicode(250), nullable=False)


class UserCommonMixin:
    """
    user common mixin class.
    """

    class GenderEnum(CoreEnum):
        FEMALE = EnumMember(0, _('Female'))
        MALE = EnumMember(1, _('Male'))
        OTHER = EnumMember(2, _('Other'))

    first_name = StringColumn(name='first_name', min_length=1, max_length=50, nullable=False)
    last_name = StringColumn(name='last_name', min_length=1, max_length=50, nullable=False)
    mobile = StringColumn(name='mobile', min_length=1, max_length=25, unique=True)
    email = StringColumn(name='email', min_length=6, max_length=50, unique=True)
    gender = SmallIntegerColumn(name='gender', check_in=GenderEnum)
    is_active = BooleanColumn(name='is_active', nullable=False, default=True)
    last_login_at = TimeStampColumn(name='last_login_at', allow_write=False)

    @hybrid_property
    def fullname(self):
        """
        gets the full name of this internal user at instance level.

        :rtype: str
        """

        return f'{self.first_name} {self.last_name}'

    @fullname.expression
    def fullname(cls):
        """
        gets the full name of this internal user at expression level.

        :rtype: str
        """

        return cls.first_name + ' ' + cls.last_name


class UserAccessMixin:
    """
    user access mixin class.
    """

    is_superuser = BooleanColumn(name='is_superuser', nullable=False, default=False)
    admin_access = BooleanColumn(name='admin_access', nullable=False, default=False)
    audit_access = BooleanColumn(name='audit_access', nullable=False, default=False)
    swagger_access = BooleanColumn(name='swagger_access', nullable=False, default=False)
