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

    :rtype: dict
    """

    return get_component(AuditPackage.COMPONENT_NAME).inspect(**options)
