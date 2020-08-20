# -*- coding: utf-8 -*-
"""
audit api module.
"""

import pyrin.audit.services as audit_services

from pyrin.api.router.decorators import api
from pyrin.core.enumerations import HTTPMethodEnum


@api('/audit', methods=HTTPMethodEnum.GET,
     authenticated=False, request_limit=5, no_cache=True)
def inspect(**options):
    """
    inspects all registered packages and gets inspection data.

    :rtype: dict
    """

    return audit_services.inspect(**options)
