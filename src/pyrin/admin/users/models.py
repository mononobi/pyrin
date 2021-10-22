# -*- coding: utf-8 -*-
"""
admin users models module.
"""

from sqlalchemy import Unicode
from sqlalchemy.ext.hybrid import hybrid_property

from pyrin.core.globals import _
from pyrin.core.enumerations import CoreEnum, EnumMember
from pyrin.database.model.mixin import HistoryMixin
from pyrin.database.model.declarative import CoreEntity
from pyrin.database.orm.sql.schema.columns import AutoPKColumn, StringColumn, \
    SmallIntegerColumn, BooleanColumn, TimeStampColumn, HiddenColumn


class AdminUserBaseEntity(CoreEntity):
    """
    admin user base entity class.
    """

    _table = 'admin_user'

    id = AutoPKColumn(name='id')


class AdminUserEntity(AdminUserBaseEntity, HistoryMixin):
    """
    admin user entity class.
    """

    _extend_existing = True

    class GenderEnum(CoreEnum):
        FEMALE = EnumMember(0, _('Female'))
        MALE = EnumMember(1, _('Male'))
        OTHER = EnumMember(2, _('Other'))

    username = StringColumn(name='username', min_length=1, max_length=30,
                            unique=True, index=True, nullable=False)
    password_hash = HiddenColumn(name='password_hash', type_=Unicode(250), nullable=False)
    first_name = StringColumn(name='first_name', min_length=1, max_length=50, nullable=False)
    last_name = StringColumn(name='last_name', min_length=1, max_length=50, nullable=False)
    mobile = StringColumn(name='mobile', min_length=1, max_length=20, unique=True)
    email = StringColumn(name='email', min_length=6, max_length=50, unique=True)
    gender = SmallIntegerColumn(name='gender', check_in=GenderEnum)
    is_active = BooleanColumn(name='is_active', nullable=False, default=True)
    is_superuser = BooleanColumn(name='is_superuser', nullable=False, default=False)
    last_login_at = TimeStampColumn(name='last_login_at', allow_write=False)

    @hybrid_property
    def fullname(self):
        """
        gets the full name of this admin user.

        :rtype: str
        """

        return f'{self.first_name} {self.last_name}'

    @fullname.expression
    def fullname(cls):
        return cls.first_name + ' ' + cls.last_name
