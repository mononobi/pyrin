# -*- coding: utf-8 -*-
"""
token manager module.
"""

import time

from jwt import decode, encode

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject, DTO
from pyrin.utils import unique_id


class TokenManager(CoreObject):
    """
    token manager class.
    """
