# -*- coding: utf-8 -*-
"""
sequence conftest module.
"""

import pytest

import pyrin.configuration.services as config_services


@pytest.fixture(scope='function')
def connection_string():
    """
    gets the connection string which is in use.

    :rtype: str
    """

    return config_services.get_active('database', 'sqlalchemy_url')
