# -*- coding: utf-8 -*-
"""
authentication models module.
"""

from sqlalchemy import BigInteger

from pyrin.database.enumerations import FKRestrictionEnum
from pyrin.database.model.mixin import HistoryMixin
from pyrin.database.model.declarative import CoreEntity
from pyrin.security.enumerations import TokenTypeEnum, InternalAuthenticatorEnum
from pyrin.database.orm.sql.schema.columns import GUIDColumn, StringColumn, \
    FKColumn, BooleanColumn


class InternalSessionBaseEntity(CoreEntity):
    """
    internal session base entity class.
    """

    _table = 'internal_session'

    id = GUIDColumn(name='id', primary_key=True, index=True)


class InternalSessionEntity(InternalSessionBaseEntity, HistoryMixin):
    """
    internal session entity class.
    """

    _extend_existing = True

    user_id = FKColumn(name='user_id', type_=BigInteger, fk='internal_user.id',
                       fk_on_delete=FKRestrictionEnum.CASCADE)
    type = StringColumn(name='type', check_in=TokenTypeEnum, nullable=False)
    authenticator = StringColumn(name='authenticator', nullable=False,
                                 check_in=InternalAuthenticatorEnum)
    is_revoked = BooleanColumn(name='is_revoked', nullable=False, default=False)
