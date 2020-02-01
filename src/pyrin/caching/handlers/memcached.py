# -*- coding: utf-8 -*-
"""
caching handlers memcached module.
"""

import pyrin.configuration.services as config_services

from pyrin.caching.handlers.base import CachingHandlerBase


class MemcachedCachingHandler(CachingHandlerBase):
    """
    memcached caching handler class.
    """

    def __init__(self, **options):
        """
        initializes an instance of MemcachedCachingHandler.
        """

        options.update(timeout=config_services.get('caching', 'memcached', 'timeout'))

        super().__init__('memcached', **options)
