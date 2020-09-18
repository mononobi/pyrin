# -*- coding: utf-8 -*-
"""
celery cli decorators module.
"""

import pyrin.task_queues.celery.cli.services as celery_cli_services


def celery_cli_handler(**options):
    """
    decorator to register a celery cli handler.

    :keyword bool replace: specifies that if there is another registered
                           cli handler with the same name, replace it
                           with the new one, otherwise raise
                           an error. defaults to False.

    :raises InvalidCLIHandlerTypeError: invalid cli handler type error.
    :raises DuplicatedCLIHandlerError: duplicated cli handler error.

    :returns: celery cli handler class.
    :rtype: CeleryCLIHandlerBase
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available celery cli handlers.

        :param CeleryCLIHandlerBase cls: celery cli handler class.

        :returns: celery cli handler class.
        :rtype: CeleryCLIHandlerBase
        """

        instance = cls()
        celery_cli_services.register_cli_handler(instance, **options)

        return cls

    return decorator
