# -*- coding: utf-8 -*-
"""
paging test_services module.
"""

import pyrin.configuration.services as config_services
import pyrin.database.paging.services as paging_services

from pyrin.core.structs import DTO


def test_enable_limit():
    """
    enables default limit parameter into given dict.
    """

    options = DTO()
    paging_services.enable_limit(options)

    assert '__limit__' in options
    assert options.get('__limit__') == config_services.get('database', 'paging', 'limit')


def test_enable_custom_limit():
    """
    enables given limit parameter into given dict.
    """

    options = DTO()
    paging_services.enable_limit(options, 2500)

    assert options.get('__limit__', None) == 2500


def test_extract_limit():
    """
    extracts and gets limit parameter from given dict.
    """

    options = DTO()
    options.update(__limit__=3000)
    limit = paging_services.extract_limit(options)

    assert limit == 3000


def test_extract_limit_none():
    """
    extracts and gets limit parameter from given
    dict. it should return the None value.
    """

    options = DTO()
    limit = paging_services.extract_limit(options)

    assert limit is None
