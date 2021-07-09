# -*- coding: utf-8 -*-
"""
swagger tags public module.
"""

from pyrin.api.router.handlers.public import PublicRoute
from pyrin.api.swagger.tags.base import BaseTag


class PublicTag(BaseTag):
    """
    public tag class.

    this tag includes all public routes.
    """

    _name = 'public'
    _tag = 'Public'

    def is_accepted(self, rule, method, **options):
        """
        gets a value indicating that this rule is accepted for this tag.

        :param pyrin.api.router.handlers.base.RouteBase rule: rule instance to be processed.
        :param str method: http method name.

        :rtype: bool
        """

        return isinstance(rule, PublicRoute)
