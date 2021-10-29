# -*- coding: utf-8 -*-
"""
security enumerations module.
"""

from pyrin.core.enumerations import CoreEnum, EnumMember


class TokenTypeEnum(CoreEnum):
    """
    token type enum.
    """

    ACCESS = 'access'
    REFRESH = 'refresh'


class InternalAuthenticatorEnum(CoreEnum):
    """
    internal authenticator enum.
    """

    ADMIN = EnumMember('admin', 'Admin')
    AUDIT = EnumMember('audit', 'Audit')
    SWAGGER = EnumMember('swagger', 'Swagger')
