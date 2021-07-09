# -*- coding: utf-8 -*-
"""
swagger tags protected module.
"""

from pyrin.api.swagger.decorators import tag
from pyrin.api.swagger.tags.base import BaseTag
from pyrin.api.router.handlers.protected import ProtectedRoute


@tag()
class ProtectedTag(BaseTag):
    """
    protected tag class.

    this tag includes all protected routes.
    """

    _name = 'protected'
    _tag = 'Protected'

    def is_accepted(self, rule, method, **options):
        """
        gets a value indicating that this rule is accepted for this tag.

        :param pyrin.api.router.handlers.base.RouteBase rule: rule instance to be processed.
        :param str method: http method name.

        :rtype: bool
        """

        return isinstance(rule, ProtectedRoute)
