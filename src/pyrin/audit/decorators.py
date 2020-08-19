# -*- coding: utf-8 -*-
"""
audit decorators module.
"""

import pyrin.audit.services as audit_services


def audit_hook():
    """
    decorator to register an audit hook.

    :raises InvalidAuditHookTypeError: invalid audit hook type error.

    :returns: audit hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available audit hooks.

        :param type cls: audit hook class.

        :returns: audit hook class.
        :rtype: type
        """

        instance = cls()
        audit_services.register_hook(instance)

        return cls

    return decorator
