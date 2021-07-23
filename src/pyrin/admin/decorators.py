# -*- coding: utf-8 -*-
"""
admin decorators module.
"""

import pyrin.admin.services as admin_services


def admin(*args, **kwargs):
    """
    decorator to register an admin page.

    :param object args: admin class constructor arguments.
    :param object kwargs: admin class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           admin page with the same register name or the same entity,
                           replace it with the new one, otherwise raise
                           an error. defaults to False.

    :raises InvalidAdminPageTypeError: invalid admin page type error.
    :raises DuplicatedAdminPageError: duplicated admin page error.

    :returns: admin class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available admin pages.

        :param type cls: admin class.

        :returns: admin class.
        :rtype: type
        """

        instance = cls(*args, **kwargs)
        admin_services.register(instance, **kwargs)

        return cls

    return decorator
