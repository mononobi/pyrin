# -*- coding: utf-8 -*-
"""
utils paging module.
"""

import pyrin.configuration.services as config_services


def inject_limit(**options):
    """
    injects default limit parameter into given keyword arguments.
    """

    inject_custom_limit(config_services.get('database', 'paging', 'limit'), **options)


def inject_custom_limit(limit, **options):
    """
    injects given limit parameter into given keyword arguments.

    :param int limit: limit value to be set in given keyword arguments.
    """

    options.update(__query_limit__=limit)


def extract_limit(**options):
    """
    extracts and gets limit parameter from given keyword arguments.

    :keyword int __query_limit__: the limit that should be set in query.
                                  defaults to value from `database.config`
                                  if not provided.

    :rtype: int
    """

    return options.get('__query_limit__', config_services.get('database', 'paging', 'limit'))
