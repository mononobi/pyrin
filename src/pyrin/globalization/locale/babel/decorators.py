# -*- coding: utf-8 -*-
"""
babel decorators module.
"""

import pyrin.globalization.locale.babel.services as babel_services


def babel_cli_handler(**options):
    """
    decorator to register a babel cli handler.

    :keyword bool replace: specifies that if there is another registered
                           cli handler with the same name, replace it
                           with the new one, otherwise raise
                           an error. defaults to False.

    :raises InvalidCLIHandlerTypeError: invalid cli handler type error.
    :raises DuplicatedCLIHandlerError: duplicated cli handler error.

    :returns: babel cli handler class.
    :rtype: BabelCLIHandlerBase
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available babel cli handlers.

        :param BabelCLIHandlerBase cls: babel cli handler class.

        :returns: babel cli handler class.
        :rtype: BabelCLIHandlerBase
        """

        instance = cls()
        babel_services.register_cli_handler(instance, **options)

        return cls

    return decorator
