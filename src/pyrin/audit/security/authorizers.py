# -*- coding: utf-8 -*-
"""
audit security authorizers module.
"""

from pyrin.core.globals import _
from pyrin.security.authorization.decorators import authorizer
from pyrin.security.enumerations import InternalAuthenticatorEnum
from pyrin.security.authorization.handlers.internal import InternalAuthorizer
from pyrin.audit.security.exceptions import AuditAccessNotAllowedError


@authorizer()
class AuditAuthorizer(InternalAuthorizer):
    """
    audit authorizer class.
    """

    _name = InternalAuthenticatorEnum.AUDIT

    def _authorize_access(self, user, **options):
        """
        authorizes the given internal user for audit access.

        :param int user: internal user id to be checked if it is authorized.

        :keyword dict user_info: internal user info to be used to check for user.

        :raises AuditAccessNotAllowedError: audit access not allowed error.
        """

        user_info = options.get('user_info')
        if not user_info or user_info.get('audit_access') is not True:
            raise AuditAccessNotAllowedError(_('You are not allowed to access the audit api. '
                                               'If you think that this is a mistake, please '
                                               'contact the support team.'))
