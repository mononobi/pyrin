# -*- coding: utf-8 -*-
"""
audit services module.
"""

from pyrin.audit import AuditPackage
from pyrin.application.services import get_component


def register_hook(instance):
    """
    registers the given instance into audit hooks.

    :param AuditHookBase instance: audit hook instance to be registered.

    :raises InvalidAuditHookTypeError: invalid audit hook type error.
    """

    return get_component(AuditPackage.COMPONENT_NAME).register_hook(instance)


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

    :keyword bool raise_error: specifies that it must raise error
                               if any of registered audits failed
                               instead of returning a failure response.
                               defaults to False if not provided.

    :raises AuditFailedError: audit failed error.

    :returns: tuple[dict(dict application: application info,
                         dict packages: loaded packages info,
                         dict framework: framework info,
                         dict python: python info,
                         dict platform: platform info),
                    int status_code]
    :rtype: tuple[dict, int]
    """

    return get_component(AuditPackage.COMPONENT_NAME).inspect(**options)


def startup_inspect():
    """
    inspects all registered packages on application startup.

    it raises an error if anything goes wrong.

    :raises AuditFailedError: audit failed error.
    """

    return get_component(AuditPackage.COMPONENT_NAME).startup_inspect()


def get_application_info(**options):
    """
    gets the info of current application.

    :returns: dict(str name: application name,
                   datetime datetime: application current datetime,
                   str version: application version)
    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).get_application_info(**options)


def get_framework_info(**options):
    """
    gets the info of current framework.

    :returns: dict(str name: framework name,
                   str version: framework version)
    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).get_framework_info(**options)


def get_python_info(**options):
    """
    gets the current python version info which application is running on it.

    :returns: dict(str version: python version,
                   str implementation: python implementation)
    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).get_python_info(**options)


def get_operating_system_info(**options):
    """
    gets the current operating system info.

    :returns: dict(str name: os name,
                   str release: os release,
                   str version: os version)
    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).get_operating_system_info(**options)


def get_hardware_info(**options):
    """
    gets the current machine's hardware info.

    :returns: dict(str processor: processor name,
                   str machine: machine name)
    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).get_hardware_info(**options)


def get_platform_info(**options):
    """
    gets the platform info of current machine.

    it includes all available info, but it could be customized using different options.

    :keyword bool os: specifies that operating system info must be included.
    :keyword bool hardware: specifies that hardware info must be included.

    :returns: dict(dict os: os info,
                   dict hardware: hardware info)
    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).get_platform_info(**options)


def get_audit_configurations():
    """
    gets the audit api configurations.

    :returns: dict(bool enabled: enable audit api,
                   bool authenticated: audit api access type,
                   int request_limit: audit api request count limit,
                   str url: audit api exposed url)
    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).get_audit_configurations()
