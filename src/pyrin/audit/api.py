# -*- coding: utf-8 -*-
"""
audit api module.
"""

import pyrin.audit.services as audit_services

from pyrin.api.router.decorators import api
from pyrin.core.enumerations import HTTPMethodEnum


audit_config = audit_services.get_audit_configurations()
is_enabled = audit_config.pop('enabled', False)

if is_enabled is True:
    @api(**audit_config, methods=HTTPMethodEnum.GET, no_cache=True)
    def inspect(**options):
        """
        inspects all registered packages and gets inspection data.

        it includes all available info, but it could be customized using different options.
        other custom implementations could also be excluded from result if the related name
        of their hook is passed with False value. for example `database=False`.

        it returns a tuple of two values. the first value is a dict containing the
        inspection data, and the second value is the related status code for the response.
        in case of any inspection has been failed, the status code will be internal
        server error 500.

        :keyword bool application: specifies that application info must be included.
        :keyword bool packages: specifies that loaded packages info must be included.
        :keyword bool framework: specifies that framework info must be included.
        :keyword bool python: specifies that python info must be included.
        :keyword bool os: specifies that operating system info must be included.
        :keyword bool hardware: specifies that hardware info must be included.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :returns: tuple[dict(dict application: application info,
                             dict packages: loaded packages info,
                             dict framework: framework info,
                             dict python: python info,
                             dict platform: platform info),
                        int status_code]
        :rtype: tuple[dict, int]
        """

        return audit_services.inspect(**options)
