# -*- coding: utf-8 -*-
"""
utils paging module.
"""

import pyrin.configuration.services as config_services


def inject_limit(options):
    """
    injects default limit parameter into given dict.

    :param dict options: options dict to inject limit into it.
    """

    inject_custom_limit(config_services.get('database', 'paging', 'limit'), options)


def inject_custom_limit(limit, options):
    """
    injects given limit parameter into given dict.

    :param int limit: limit value to be set in given dict.
    :param dict options: options dict to inject limit into it.
    """

    options.update(__limit__=limit)


def extract_limit(options):
    """
    extracts and gets limit parameter from given dict.
    if `__limit__` key is not available in provided
    dict, it gets the value from `database.config` file `paging` section.

    :param dict options: options dict to get limit from it.

    :rtype: int
    """

    return options.get('__limit__', config_services.get('database', 'paging', 'limit'))
