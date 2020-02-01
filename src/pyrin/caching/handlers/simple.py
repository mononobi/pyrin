# -*- coding: utf-8 -*-
"""
caching handlers simple module.
"""

import pyrin.configuration.services as config_services

from pyrin.caching.handlers.base import DictCachingHandlerBase


class SimpleCachingHandler(DictCachingHandlerBase):
    """
    simple caching handler class.
    """

    def __init__(self, **options):
        """
        initializes an instance of DictCachingHandlerBase.
        """

        options.update(timeout=config_services.get('caching', 'simple', 'timeout'),
                       max_length=config_services.get('caching', 'simple', 'max_length'))

        super().__init__('simple', **options)
