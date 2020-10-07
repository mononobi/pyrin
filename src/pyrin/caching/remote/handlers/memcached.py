# -*- coding: utf-8 -*-
"""
caching remote handlers memcached module.
"""

import pickle

from pymemcache import Client

from pyrin.caching.decorators import cache
from pyrin.caching.exceptions import InvalidCacheLimitError
from pyrin.caching.globals import NO_LIMIT
from pyrin.caching.remote.handlers.base import RemoteCacheBase
from pyrin.caching.remote.handlers.exceptions import HostnameOrUnixSocketRequiredError, \
    BothHostnameAndUnixSocketProvidedError


@cache()
class Memcached(RemoteCacheBase):
    """
    memcached class.
    """

    cache_name = 'memcached'

    HIT_KEY = '__HIT_COUNT__'
    MISS_KEY = '__MISS_COUNT__'

    def __init__(self, *args, **options):
        """
        initializes an instance of Memcached.

        :keyword int limit: limit for memory usage by cached items in megabytes.
                            if not provided, it will be get from
                            `caching` config store. if you want to
                            remove size limit, you could pass
                            `caching.globals.NO_LIMIT` as input. note
                            that this will remove limit only by client,
                            so memcached server default limit will be intact.

        :keyword int expire: default expire time of cached items in seconds.
                             if not provided, it will be get from `caching` config
                             store.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.

        :raises CacheNameIsRequiredError: cache name is required error.
        :raises InvalidCacheExpireTimeError: invalid cache expire time error.
        :raises InvalidCacheLimitError: invalid cache limit error.
        """

        self._limit = NO_LIMIT

        super().__init__(*args, **options)

        self.client.add(self.HIT_KEY, 0, expire=0, noreply=True, flags=1)
        self.client.add(self.MISS_KEY, 0, expire=0, noreply=True, flags=1)

    def _create_client(self, *args, kwargs=None, **configs):
        """
        creates a client for connecting to memcached server.

        :param object args: all positional arguments passed to `__init__` method.
        :param dict kwargs: all keyword arguments passed to `__init__` method.

        :keyword int limit: limit for memory usage by cached items in megabytes.
                            if not provided, it will be get from
                            `caching` config store. if you want to
                            remove size limit, you could pass
                            `caching.globals.NO_LIMIT` as input. note
                            that this will remove limit only by client,
                            so memcached server default limit will be intact.

        :keyword str hostname: the host name of memcached server. it could be
                               ip, url or `localhost`.

        :keyword int port: port number of memcached server.

        :keyword str unixsocket: path to unix socket file.

        :note hostname, port and unixsocket: both unixsocket and hostname, port
                                             could not be provided at the same time.

        :keyword int connect_timeout: milliseconds to wait for a connection to
                                      the memcached server. defaults to `forever`
                                      (uses the underlying default socket timeout,
                                      which can be very long).

        :keyword int timeout: milliseconds to wait for send or recv calls on
                              the socket connected to memcached. defaults to
                              `forever` (uses the underlying default socket
                              timeout, which can be very long).

        :keyword bool no_delay: set the TCP_NODELAY flag, which may help with
                                performance in some cases. defaults to False.

        :keyword bool ignore_exc: True to cause the `get`, `gets`, `get_many` and
                                  `gets_many` calls to treat any errors as cache
                                  misses. defaults to False.

        :keyword bool default_noreply: the default value for `noreply` as passed to
                                       store commands (except from cas, incr, and decr,
                                       which default to False).

        :keyword bool allow_unicode_keys: support unicode (utf8) keys.
        :keyword str encoding: controls data encoding. defaults to `ascii`.

        :raises InvalidCacheLimitError: invalid cache limit error.

        :raises BothHostnameAndUnixSocketProvidedError: both hostname and unix
                                                        socket provided error.

        :raises HostnameOrUnixSocketRequiredError: hostname or unix socket
                                                   required error.

        :rtype: pymemcache.Client
        """

        if kwargs is None:
            kwargs = {}

        limit = kwargs.get('limit') or configs.pop('limit', None)
        if limit is None or (limit != NO_LIMIT and limit <= 0):
            raise InvalidCacheLimitError('Cache limit for cache [{name}] '
                                         'must be a positive integer.'
                                         .format(name=self.get_name()))
        self._limit = limit

        # we should remove 'limit' from configs to be able to pass it to Client initializer.
        configs.pop('limit', None)

        unixsocket = configs.pop('unixsocket', None)
        hostname = configs.pop('hostname', None)
        port = configs.pop('port', None)

        if unixsocket is not None and (hostname is not None or port is not None):
            raise BothHostnameAndUnixSocketProvidedError('Both hostname and unix socket could '
                                                         'not be provided at the same time.')

        if unixsocket is None and (hostname is None or port is None):
            raise HostnameOrUnixSocketRequiredError('Hostname or unix socket must be provided '
                                                    'to connect to memcached server.')

        server = None
        if unixsocket is not None:
            server = unixsocket
        else:
            server = hostname, port

        timeout = configs.get('timeout')
        if timeout is not None and timeout > 0:
            timeout = timeout / 1000
            configs.update(timeout=timeout)

        connect_timeout = configs.get('connect_timeout')
        if connect_timeout is not None and connect_timeout > 0:
            connect_timeout = connect_timeout / 1000
            configs.update(connect_timeout=connect_timeout)

        configs.update(serde=self)
        client = Client(server, **configs)
        if self.limit != NO_LIMIT:
            client.cache_memlimit(self.limit)

        return client

    def _increase_hit(self):
        """
        increases hit count of this cache.
        """

        self.client.incr(self.HIT_KEY, 1, noreply=True)

    def _increase_miss(self):
        """
        increases miss count of this cache.
        """

        self.client.incr(self.MISS_KEY, 1, noreply=True)

    def _clear(self):
        """
        clears all items from cache.
        """

        self.client.flush_all(noreply=True)

    def _set(self, key, value, *args, **options):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :keyword int expire: expire time for this item in seconds.
                             if not provided, it will be get from `expire` attribute.

        :keyword bool noreply: True to not wait for the reply. if not
                               provided, defaults to `caching` config store.

        :keyword int flags: arbitrary bit field used for memcached server-specific flags.
        """

        expire = options.get('expire')
        if expire is None:
            expire = self.expire

        self.client.set(key, value, expire=expire,
                        noreply=options.get('noreply'),
                        flags=options.get('flags'))

    def _get(self, key, default=None, **options):
        """
        gets the value from cache.

        if key does not exist, it returns None or the specified default value.

        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        result = self.client.get(key, default=default)
        if result in (None, default):
            self._increase_miss()
            return result

        self._increase_hit()
        return result

    def _prepare_key(self, key):
        """
        prepares the key to be used in cache.

        :param object key: key to be cached.

        :returns: prepared key.
        :rtype: str
        """

        return str(key)

    def serialize(self, key, value):
        """
        serializes the given value.

        :param object key: key of value to be serialized.
        :param object value: value to be serialized.

        :returns: serialized value
        :rtype: tuple[bytes | int, int]
        """

        if isinstance(value, int):
            return value, 1

        return pickle.dumps(value), 2

    def deserialize(self, key, value, flags=None):
        """
        deserializes the given value.

        :param object key: key of value to be deserialized.
        :param bytes value: value to be deserialized.

        :param int flags: bitwise flags. if you want to deserialize
                          an integer value, you could set it to 1.

        :returns: deserialized value
        """

        if flags == 1:
            return int(value)

        return pickle.loads(value)

    def increment(self, key, value, noreply=False):
        """
        increments the value of given key by provided value.

        the cached and provided values must be integers.
        it returns the new value if key is existed, otherwise returns None.
        note that if noreply=True, it always returns None.

        :param object key: hashable key to increase its value in the cache.
        :param int value: the amount by which to increment the cached value.
        :param bool noreply: True to not wait for the reply. defaults to False.

        :rtype: int
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        return self.client.incr(hashed_key, value, noreply)

    def decrement(self, key, value, noreply=False):
        """
        decrements the value of given key by provided value.

        the cached and provided values must be integers.
        it returns the new value if key is existed, otherwise returns None.
        note that if noreply=True, it always returns None.

        :param object key: hashable key to decrease its value in the cache.
        :param int value: the amount by which to decrement the cached value.
        :param bool noreply: True to not wait for the reply. defaults to False.

        :rtype: int
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        return self.client.decr(hashed_key, value, noreply)

    def contains(self, key):
        """
        gets a value indicating that given key is existed in the cached items.

        :param object key: key to be checked for existence.

        :rtype: bool
        """

        result = self.get(key, default=None)
        return result is not None

    def pop(self, key, default=None):
        """
        pops the given key from cache and returns its value.

        if key does not exist, it returns None or the specified default value.

        :param object key: key to get its value.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        result = self.get(key, default=default)
        self.remove(key, noreply=True)
        return result

    def remove(self, key, **options):
        """
        removes the given key from cache.

        it does nothing if the key is not present in the cache.

        :keyword bool noreply: do not wait for reply from server.
                               will be get from `caching` config store
                               if not provided.

        :param object key: key to be removed.
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        self.client.delete(hashed_key, noreply=options.get('noreply'))

    def touch(self, key, expire=0, noreply=None):
        """
        extends the expire time of given key in the cache.


        :param object key: hashable key to extend its expire time.

        :param int expire: expire time for this item in seconds.
                           if not provided, it will be get from `expire` attribute.

        :param bool noreply: True to not wait for the reply. if not
                             provided, defaults to `caching` config store.

        :returns: True if expire time updated, False if the key is not existed.
        :rtype: bool
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)

        if expire is None:
            expire = self.expire

        return self.client.touch(hashed_key, expire=expire, noreply=noreply)

    def add(self, key, value, expire=0, noreply=None, flags=None):
        """
        adds the given key into the cache if it isn't already, otherwise does nothing.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :param int expire: expire time for this item in seconds.
                           if not provided, it will be get from `expire` attribute.

        :param bool noreply: True to not wait for the reply. if not
                             provided, defaults to `caching` config store.

        :param int flags: arbitrary bit field used for memcached server-specific flags.

        :returns: True if value is set, False if the key is already existed.
        :rtype: bool
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)

        if expire is None:
            expire = self.expire

        return self.client.add(hashed_key, value, expire=expire, noreply=noreply, flags=flags)

    @property
    def stats(self):
        """
        get the statistic info about cached items.

        :returns: dict(datetime last_cleared_time: last cleared time,
                       bool persistent: persistent cache,
                       bool consider_user: consider user,
                       int expire: cached items expire time,
                       int hit: hit count,
                       int miss: miss count,
                       str hit_ratio: hit ratio,
                       int limit: memory size limit)
        :rtype: dict
        """

        base_stats = super().stats
        stats = dict(limit=self.limit)
        base_stats.update(stats)
        return base_stats

    @property
    def hit_count(self):
        """
        gets the hit count for this cache.

        :rtype: int
        """

        return self.client.get(self.HIT_KEY, default=0)

    @property
    def miss_count(self):
        """
        gets the miss count for this cache.

        :rtype: int
        """

        return self.client.get(self.MISS_KEY, default=0)

    @property
    def limit(self):
        """
        gets the memory size limit of this cache in megabytes.

        :rtype: int
        """

        return self._limit
