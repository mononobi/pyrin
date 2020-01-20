# -*- coding: utf-8 -*-
"""
permission models module.
"""

from sqlalchemy import Unicode, SmallInteger

from pyrin.core.context import DTO
from pyrin.database.model.base import CoreEntity
from pyrin.database.model.schema import CoreColumn


class PermissionBaseEntity(CoreEntity):
    """
    permission base entity class.
    """

    __tablename__ = 'permission'

    id = CoreColumn(name='id', type_=SmallInteger, primary_key=True, nullable=False, index=True)

    def primary_key(self):
        """
        gets the primary key of this instance.

        :rtype: int
        """

        return self.id


class PermissionEntity(PermissionBaseEntity):
    """
    permission entity class.
    """

    __table_args__ = DTO(extend_existing=True)

    description = CoreColumn(name='description', type_=Unicode(100), nullable=False)
