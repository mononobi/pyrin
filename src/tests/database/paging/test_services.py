# -*- coding: utf-8 -*-
"""
paging test_services module.
"""

import pyrin.configuration.services as config_services
import pyrin.database.paging.services as paging_services

from pyrin.core.context import DTO


def test_inject_limit():
    """
    injects default limit parameter into given dict.
    """

    options = DTO()
    paging_services.inject_limit(options)

    assert '__limit__' in options
    assert options.get('__limit__') == config_services.get('database', 'paging', 'limit')


def test_inject_custom_limit():
    """
    injects given limit parameter into given dict.
    """

    options = DTO()
    paging_services.inject_custom_limit(2500, options)

    assert options.get('__limit__', None) == 2500


def test_extract_limit():
    """
    extracts and gets limit parameter from given dict.
    """

    options = DTO()
    options.update(__limit__=3000)
    limit = paging_services.extract_limit(options)

    assert limit == 3000


def test_extract_limit_default():
    """
    extracts and gets limit parameter from given dict.
    it should return the default value from `database.config`.
    """

    options = DTO()
    limit = paging_services.extract_limit(options)

    assert limit == config_services.get('database', 'paging', 'limit')
