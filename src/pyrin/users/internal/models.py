# -*- coding: utf-8 -*-
"""
users internal models module.
"""

from pyrin.database.model.mixin import HistoryMixin
from pyrin.database.model.declarative import CoreEntity
from pyrin.users.mixin import UserPKMixin, UserCommonMixin, UserAccessMixin, \
    UserCredentialMixin


class InternalUserEntity(CoreEntity, UserPKMixin,
                         UserCredentialMixin, UserCommonMixin,
                         UserAccessMixin, HistoryMixin):
    """
    internal user entity class.
    """

    _table = 'internal_user'
