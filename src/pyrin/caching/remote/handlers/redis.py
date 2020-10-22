# -*- coding: utf-8 -*-
"""
caching remote handlers redis module.
"""

import pickle

import redis

from pyrin.caching.decorators import cache
from pyrin.caching.remote.handlers.base import RemoteCacheBase
from pyrin.caching.remote.handlers.exceptions import HostnameOrUnixSocketRequiredError, \
    BothHostnameAndUnixSocketProvidedError


@cache()
class Redis(RemoteCacheBase):
    """
    redis class.
    """

    cache_name = 'redis'

    HIT_KEY = '__HIT_COUNT__'
    MISS_KEY = '__MISS_COUNT__'

    def __init__(self, *args, **options):
        """
        initializes an instance of Redis.

        :keyword int expire: default expire time of cached items in milliseconds.
                             if not provided, it will be get from `caching` config
                             store.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.

        :raises CacheNameIsRequiredError: cache name is required error.
        :raises InvalidCacheExpireTimeError: invalid cache expire time error.
        """

        super().__init__(*args, **options)

        self.client.set(self.HIT_KEY, 0)
        self.client.set(self.MISS_KEY, 0)

    def _create_client(self, *args, kwargs=None, **configs):
        """
        creates a client for connecting to redis server.

        :param object args: all positional arguments passed to `__init__` method.
        :param dict kwargs: all keyword arguments passed to `__init__` method.

        :keyword str host: the host name of redis server. it could be
                           ip, url or `localhost`.

        :keyword int port: port number of redis server.

        :keyword str unix_socket_path: path to unix socket file.

        :note host, port and unix_socket_path: both unix_socket_path and host, port
                                               could not be provided at the same time.

        :keyword int socket_connect_timeout: milliseconds to wait for a connection to
                                             the redis server. defaults to `forever`
                                             (uses the underlying default socket timeout,
                                             which can be very long).

        :keyword int socket_timeout: milliseconds to wait for send or recv calls on
                                     the socket connected to redis. defaults to
                                     `forever` (uses the underlying default socket
                                     timeout, which can be very long).

        :keyword bool retry_on_timeout: retry on tcp connection timeout for
                                        sending/receiving values.

        :keyword str encoding: controls data encoding.
        :keyword str encoding_errors: how to face encoding errors.
        :keyword int db: specify a database number.
        :keyword str username: tcp connection username.
        :keyword str password: tcp connection password.
        :keyword bool socket_keepalive: keep-alive tcp connection.
        :keyword dict socket_keepalive_options: tcp keep-alive options.
        :keyword bool decode_responses: decode responses.
        :keyword bool ssl: use ssl connection to server.
        :keyword str ssl_keyfile: path to ssl key file.
        :keyword str ssl_certfile: path to ssl cert file.
        :keyword str ssl_cert_reqs: require certificate in connection.
        :keyword str ssl_ca_certs: path to the CA certificate.
        :keyword bool ssl_check_hostname: ssl check hostname.
        :keyword int max_connections: max connections to redis server.
        :keyword bool single_connection_client: create a single connection client.
        :keyword int health_check_interval: health check interval in seconds.
        :keyword str client_name: redis client name.

        :raises BothHostnameAndUnixSocketProvidedError: both hostname and unix
                                                        socket provided error.

        :raises HostnameOrUnixSocketRequiredError: hostname or unix socket
                                                   required error.

        :rtype: redis.Redis
        """

        unix_socket_path = configs.get('unix_socket_path', None)
        host = configs.get('host', None)
        port = configs.get('port', None)

        if unix_socket_path is not None and (host is not None or port is not None):
            raise BothHostnameAndUnixSocketProvidedError('Both host and unix socket could '
                                                         'not be provided at the same time.')

        if unix_socket_path is None and (host is None or port is None):
            raise HostnameOrUnixSocketRequiredError('Host or unix socket must be provided '
                                                    'to connect to redis server.')

        socket_timeout = configs.get('socket_timeout')
        if socket_timeout is not None and socket_timeout > 0:
            socket_timeout = socket_timeout / 1000
            configs.update(socket_timeout=socket_timeout)

        socket_connect_timeout = configs.get('socket_connect_timeout')
        if socket_connect_timeout is not None and socket_connect_timeout > 0:
            socket_connect_timeout = socket_connect_timeout / 1000
            configs.update(socket_connect_timeout=socket_connect_timeout)

        client = redis.Redis(**configs)
        return client

    def _increase_hit(self):
        """
        increases hit count of this cache.
        """

        self.client.incr(self.HIT_KEY, 1)

    def _increase_miss(self):
        """
        increases miss count of this cache.
        """

        self.client.incr(self.MISS_KEY, 1)

    def _clear(self):
        """
        clears all items from cache.
        """

        self.client.flushdb(asynchronous=True)

    def _set(self, key, value, *args, **options):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :keyword int expire: expire time for this item in milliseconds.
                             if not provided, it will be get from `expire` attribute.
        """

        expire = options.get('expire')
        if expire is None:
            expire = self.expire

        if expire == 0:
            expire = None

        self.client.set(key, value, px=expire)

    def _get(self, key, default=None, **options):
        """
        gets the value from cache.

        if key does not exist, it returns None or the specified default value.

        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        result = self.client.get(key)
        if result is None:
            self._increase_miss()
            return default

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

    def _prepare_for_set(self, value):
        """
        prepares the value that must be cached.

        :param object value: value to be cached.

        :returns: prepared value
        :rtype: bytes
        """

        return pickle.dumps(value)

    def _prepare_for_get(self, value):
        """
        prepares the value that must be returned from cache.

        :param bytes value: value to be returned.

        :returns: prepared value.
        """

        return pickle.loads(value)

    def increment(self, key, value):
        """
        increments the value of given key by provided value.

        if the key does not exist, it will be initialized by value.
        the cached and provided values must be integers.
        it returns the new value.

        :param object key: hashable key to increase its value in the cache.
        :param int value: the amount by which to increment the cached value.

        :rtype: int
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        return self.client.incr(hashed_key, value)

    def decrement(self, key, value):
        """
        decrements the value of given key by provided value.

        if the key does not exist, it will be initialized as 0.
        the cached and provided values must be integers.
        it returns the new value.

        :param object key: hashable key to decrease its value in the cache.
        :param int value: the amount by which to decrement the cached value.

        :rtype: int
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        return self.client.decr(hashed_key, value)

    def contains(self, key):
        """
        gets a value indicating that given key is existed in the cached items.

        :param object key: key to be checked for existence.

        :rtype: bool
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        result = self.client.exists(hashed_key)
        return result > 0

    def pop(self, key, default=None):
        """
        pops the given key from cache and returns its value.

        if key does not exist, it returns None or the specified default value.

        :param object key: key to get its value.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        result = self.get(key, default=default)
        self.remove(key)
        return result

    def remove(self, key, **options):
        """
        removes the given key from cache.

        it does nothing if the key is not present in the cache.

        :param object key: key to be removed.
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        self.client.delete(hashed_key)

    def touch(self, key):
        """
        extends the expire time of given key in the cache.

        :param object key: hashable key to extend its expire time.

        :returns: True if expire time updated, False if the key is not existed.
        :rtype: bool
        """

        hashed_key = hash(key)
        hashed_key = self._prepare_key(hashed_key)
        return self.client.touch(hashed_key)

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
                       dict memory_stats: memory stats)
        :rtype: dict
        """

        base_stats = super().stats
        stats = dict(memory_stats=self.client.memory_stats())
        base_stats.update(stats)
        return base_stats

    @property
    def hit_count(self):
        """
        gets the hit count for this cache.

        :rtype: int
        """

        return int(self.client.get(self.HIT_KEY) or 0)

    @property
    def miss_count(self):
        """
        gets the miss count for this cache.

        :rtype: int
        """

        return int(self.client.get(self.MISS_KEY) or 0)
