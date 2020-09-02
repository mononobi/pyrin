# -*- coding: utf-8 -*-
"""
caching handlers base module.
"""

from abc import abstractmethod

import pyrin.configuration.services as config_services
import pyrin.globalization.datetime.services as datetime_services
import pyrin.security.session.services as session_services
import pyrin.utils.function as func_utils

from pyrin.caching.structs import CacheableDict
from pyrin.caching.globals import NO_LIMIT
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.caching.items.base import CacheItemBase, ComplexCacheItemBase
from pyrin.caching.containers.base import CachingContainerBase
from pyrin.caching.interface import AbstractCachingHandler, AbstractComplexCachingHandler, \
    AbstractExtendedCachingHandler
from pyrin.caching.handlers.exceptions import CacheNameIsRequiredError, \
    InvalidCachingContainerTypeError, InvalidCacheItemTypeError, InvalidCacheLimitError, \
    InvalidCacheTimeoutError, InvalidCacheClearCountError, CacheClearanceLockTypeIsRequiredError


class CachingHandlerBase(AbstractCachingHandler):
    """
    caching handler base class.

    this type of caching handlers does not consider method inputs, current
    user and component key in key generation. it only considers the class
    type of function and function name itself. this is useful for caching
    items that never change after application startup and are independent
    from different scoped or global variables.

    it also does not support timeout and size limit for cached values.
    its values are permanent unless manually removed if required.

    it also keeps the real value in the cache, not a deep copy of it to gain
    performance.

    it also does not provide statistic info about hit or missed
    caches, to gain performance.
    """

    # cache name to be used for this handler.
    # it must be unique between all caching handlers.
    cache_name = None

    # a class type to be used as cache container.
    # it could be overridden in subclasses.
    container_class = None

    # a class type to hold each item in the cache.
    # it could be overridden in subclasses.
    cache_item_class = None

    def __init__(self, *args, **options):
        """
        initializes an instance of CachingHandlerBase.

        :raises InvalidCachingContainerTypeError: invalid caching container type error.
        :raises InvalidCacheItemTypeError: invalid cache item type error.
        :raises CacheNameIsRequiredError: cache name is required error.
        """

        super().__init__()

        if self.container_class is None or \
                not issubclass(self.container_class, CachingContainerBase):
            raise InvalidCachingContainerTypeError('Provided caching container [{container}] '
                                                   'is not a subclass of [{base}].'
                                                   .format(container=self.container_class,
                                                           base=CachingContainerBase))

        if self.cache_item_class is None or \
                not issubclass(self.cache_item_class, CacheItemBase):
            raise InvalidCacheItemTypeError('Provided cache item [{item}] '
                                            'is not a subclass of [{base}].'
                                            .format(item=self.cache_item_class,
                                                    base=CacheItemBase))

        if self.cache_name in (None, '') or self.cache_name.isspace():
            raise CacheNameIsRequiredError('Cache name must be provided.')

        self._container = self.container_class()
        self._set_name(self.cache_name)
        self._last_cleared_time = datetime_services.now()

    def _get_parent_type(self, parent):
        """
        gets the parent type from given input.

        if it is a class itself, it returns the same input.

        :param type | object parent: class or instance to get its type.

        :rtype: type
        """

        parent_type = parent
        if not isinstance(parent_type, type):
            parent_type = type(parent_type)

        return parent_type

    def _get_cache_item(self, value, *args, **options):
        """
        gets the equivalent cache item for given value.

        :param object value: value to be cached.

        :rtype: CacheItemBase
        """

        return self.cache_item_class(value, *args, **options)

    def _get_configs(self):
        """
        gets the configs of this handler from `caching` config store.

        first, it checks if a section with the name of this handler
        is present in config store. if so, it returns the values from it.
        otherwise it returns the result of `_get_default_configs` method.

        :rtype: dict
        """

        if self.get_name() in config_services.get_section_names('caching'):
            return config_services.get_section('caching', self.get_name())
        else:
            return self._get_default_configs()

    @abstractmethod
    def _get_default_configs(self):
        """
        gets the defaults configs of this handler from `caching` config store.

        this method must be overridden in subclasses to provide custom configs if
        a section with the handler name is not present in config store.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: dict
        """

        raise CoreNotImplementedError('This method must be implemented in '
                                      '[{class_name}] class to provide default '
                                      'configs for caching handler [{name}].'
                                      .format(class_name=self, name=self.get_name()))

    def set(self, key, value, *args, **options):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.
        """

        hash_key = hash(key)
        cache_item = self._get_cache_item(hash_key, value, *args, **options)
        self._container[hash_key] = cache_item

    def get(self, key, default=None, **options):
        """
        gets the value from cache.

        if key does not exist, it returns None or the specified default value.

        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        result = self._container.get(hash(key), default)
        if result not in (None, default):
            return result.value

        return result

    def try_set(self, value, func, parent, *args, **options):
        """
        sets a new value into cached items.

        this method will generate cache key from given type and function.

        :param object value: value to be cached.
        :param function func: function to cache its result.
        :param type | object parent: parent class or instance of given function.
        """

        key = self.generate_key(func, parent, *args, **options)
        self.set(key, value, **options)

    def try_get(self, func, parent, *args, default=None, **options):
        """
        gets the value from cache.

        this method will generate cache key from given type and function.
        if key does not exist, it returns None or the specified default value.

        :param function func: function to to get its result.
        :param type | object parent: parent class or instance of given function.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        key = self.generate_key(func, parent, *args, **options)
        return self.get(key, default=default, **options)

    def contains(self, key):
        """
        gets a value indicating that given key is existed in the cached items.

        :param object key: key to be checked for existence.

        :rtype: bool
        """

        return hash(key) in self._container

    def pop(self, key, default=None):
        """
        pops the given key from cache and returns its value.

        if key does not exist, it returns None or the specified default value.

        :param object key: key to get its value.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        return self._container.pop(hash(key), default)

    def remove(self, key):
        """
        removes the given key from cache.

        it does nothing if the key is not present in the cache.

        :param object key: key to be removed.
        """

        try:
            del self._container[hash(key)]
        except Exception:
            pass

    def clear(self):
        """
        clears all items from cache.
        """

        self._container.clear()
        self._last_cleared_time = datetime_services.now()

    def items(self):
        """
        gets an iterable of all keys and their values in the cache.

        :returns: iterable[tuple[object, object]]
        """

        return self._container.items()

    def keys(self):
        """
        gets all keys of current cache.

        :returns: iterable[object]
        """

        return self._container.keys()

    def values(self):
        """
        gets all values of current cache.

        :returns: iterable[object]
        """

        return self._container.values()

    def generate_key(self, func, parent, *args, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to to get its result.
        :param type | object parent: parent class or instance of given function.

        :returns: hash of generated key.
        :rtype: int
        """

        parent_type = None
        name = func.__name__
        if parent is None:
            name = func_utils.get_fully_qualified_name(func)
        else:
            parent_type = self._get_parent_type(parent)

        return hash((parent_type, name))

    @property
    def count(self):
        """
        gets the count of items of this handler.

        :rtype: int
        """

        return len(self._container)

    @property
    def last_cleared_time(self):
        """
        gets the last time in which this handler has been cleared.

        :rtype: datetime.datetime
        """

        return self._last_cleared_time

    @property
    def stats(self):
        """
        get the statistic info about cached items.

        :returns: dict(int count: items count,
                       datetime last_cleared_time: last cleared time)
        :rtype: dict
        """

        return dict(count=self.count,
                    last_cleared_time=self.last_cleared_time)


class ExtendedCachingHandlerBase(CachingHandlerBase, AbstractExtendedCachingHandler):
    """
    extended caching handler base class.

    this type of caching handlers are same as `CachingHandlerBase` type
    but it also considers method inputs, current user and component key in key generation.
    """

    def __init__(self, *args, **options):
        """
        initializes an instance of ExtendedCachingHandlerBase.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.

        :raises InvalidCachingContainerTypeError: invalid caching container type error.
        :raises InvalidCacheItemTypeError: invalid cache item type error.
        :raises CacheNameIsRequiredError: cache name is required error.
        """

        super().__init__(*args, **options)

        consider_user = options.get('consider_user')
        if consider_user is None:
            configs = self._get_configs()
            consider_user = configs.get('consider_user')

        self._consider_user = consider_user

    def _get_default_configs(self):
        """
        gets the defaults configs of this handler from `caching` config store.

        :rtype: dict
        """

        return config_services.get_section('caching', 'extended.permanent')

    def try_set(self, value, func, inputs, kw_inputs, *args, **options):
        """
        sets a new value into cached items.

        this method will generate cache key from given type and function
        and inputs. it also considers current component key in key generation.

        :param object value: value to be cached.
        :param function func: function to cache its result.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `caching` config
                                     store if not provided.
        """

        key = self.generate_key(func, inputs, kw_inputs, *args, **options)
        self.set(key, value, **options)

    def try_get(self, func, inputs, kw_inputs, *args, default=None, **options):
        """
        gets the value from cache.

        this method will generate cache key from given type and function
        and inputs. it also considers current component key in key generation.
        if key does not exist, it returns None or the specified default value.

        :param function func: function to to get its result.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.
        :param object default: value to be returned if key is not present.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `caching` config
                                     store if not provided.

        :returns: object
        """

        key = self.generate_key(func, inputs, kw_inputs, *args, **options)
        return self.get(key, default, **options)

    def generate_key(self, func, inputs, kw_inputs, *args, **options):
        """
        generates a cache key from given inputs.

        :param function func: function to to get its result.
        :param tuple inputs: function positional arguments.
        :param dict kw_inputs: function keyword arguments.

        :keyword bool consider_user: specifies that current user must be included in
                                     key generation. it will be get from `caching` config
                                     store if not provided.

        :returns: hash of generated key.
        :rtype: int
        """

        consider_user = options.get('consider_user', self.consider_user)
        current_user = None
        if consider_user is not False:
            current_user = session_services.get_safe_current_user()

        cacheable_inputs, parent = func_utils.get_inputs(func, inputs, kw_inputs,
                                                         CacheableDict)

        parent_type = None
        name = func.__name__
        if parent is None:
            name = func_utils.get_fully_qualified_name(func)
        else:
            parent_type = self._get_parent_type(parent)

        component_key = session_services.get_safe_component_custom_key()
        return hash((parent_type, name, cacheable_inputs, current_user, component_key))

    @property
    def consider_user(self):
        """
        gets the consider user value for this handler.

        :rtype: bool
        """

        return self._consider_user


class ComplexCachingHandlerBase(ExtendedCachingHandlerBase, AbstractComplexCachingHandler):
    """
    complex caching handler base class.

    this type of caching handlers will also consider method inputs, current user
    and component key in key generation. this is useful for caching items that change
    during application runtime based on different inputs and variables.

    it also supports timeout and size limit for cached items.
    it also keeps a deep copy of the value in the cache.
    it also provides statistic info about hit or missed caches.
    """

    # a lock type to be used on clearing cached items when cache limit is reached.
    clearance_lock_class = None

    def __init__(self, *args, **options):
        """
        initializes an instance of ComplexCachingHandlerBase.

        :keyword int limit: limit count of cached items.
                            if not provided, it will be get
                            from `caching` config store.
                            if you want to remove count limit,
                            you could pass `caching.globals.NO_LIMIT`
                            as input.

        :keyword int timeout: default timeout of cached items.
                              if not provided, it will be get
                              from `caching` config store.

        :keyword bool use_lifo: specifies that items of the cache must
                                be removed in lifo order. if not provided,
                                it will be get from `caching` config store.

        :keyword int clear_count: number of old items to be removed from cache when
                                  the cache is full. if not provided, it will be get
                                  from `caching` config store.
                                  note that reducing this value to extremely low values
                                  will cause a performance issue when the cache becomes full.

        :keyword bool consider_user: specifies that current user must also be
                                     included in cache key. if not provided, will
                                     be get from `caching` config store.

        :raises InvalidCachingContainerTypeError: invalid caching container type error.
        :raises InvalidCacheItemTypeError: invalid cache item type error.
        :raises CacheNameIsRequiredError: cache name is required error.
        :raises CacheClearanceLockTypeIsRequiredError: cache clearance lock type
                                                       is required error.
        :raises InvalidCacheLimitError: invalid cache limit error.
        :raises InvalidCacheTimeoutError: invalid cache timeout error.
        :raises InvalidCacheClearCountError: invalid cache clear count error.
        """

        super().__init__(*args, **options)

        if self.cache_item_class is None or \
                not issubclass(self.cache_item_class, ComplexCacheItemBase):
            raise InvalidCacheItemTypeError('Provided cache item [{item}] '
                                            'is not a subclass of [{base}].'
                                            .format(item=self.cache_item_class,
                                                    base=ComplexCacheItemBase))

        if self.clearance_lock_class is None:
            raise CacheClearanceLockTypeIsRequiredError('Cache clearance lock type is '
                                                        'required for complex caching '
                                                        'handlers.')

        self._clearance_lock = self.clearance_lock_class()
        self._miss_count = 0
        self._hit_count = 0

        limit = options.get('limit')
        timeout = options.get('timeout')
        use_lifo = options.get('use_lifo')
        clear_count = options.get('clear_count')

        configs = self._get_configs()
        if limit is None:
            limit = configs.get('limit')

        if timeout is None:
            timeout = configs.get('timeout')

        if use_lifo is None:
            use_lifo = configs.get('use_lifo')

        if clear_count is None:
            clear_count = configs.get('clear_count')

        if limit != NO_LIMIT and limit <= 0:
            raise InvalidCacheLimitError('Cache limit must be a positive integer.')

        if timeout <= 0:
            raise InvalidCacheTimeoutError('Cache timeout must be a positive integer.')

        if clear_count <= 0:
            raise InvalidCacheClearCountError('Cache clear count must be a positive integer.')

        self._limit = limit
        self._timeout = timeout
        self._use_lifo = use_lifo
        self._clear_count = clear_count

    def _get_default_configs(self):
        """
        gets the defaults configs of this handler from `caching` config store.

        :rtype: dict
        """

        return config_services.get_section('caching', 'complex')

    def _get_hit_ratio(self):
        """
        gets hit ratio for this handler in percentage.

        :rtype: float
        """

        hit = self.hit_count
        miss = self.miss_count
        if hit == 0 and miss == 0:
            return 0

        ratio = hit / (hit + miss)
        return ratio * 100

    def _remove_old_items(self):
        """
        removes old items from cache.

        the number of old items to be removed is calculated
        considering the `caching` config store.
        """

        with self._clearance_lock:
            is_full, count = self.is_full
            if is_full is True:
                to_be_removed = self._container.slice(count, self._use_lifo)
                for key in to_be_removed:
                    self.remove(key)

    def set(self, key, value, **options):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.

        :keyword int timeout: timeout for given key in milliseconds.
                              defaults to `timeout` attribute if not provided.
        """

        timeout = options.get('timeout')
        if timeout is None:
            timeout = self.timeout
            options.update(timeout=timeout)

        is_full, count = self.is_full
        if is_full is True:
            self._remove_old_items()

        super().set(key, value, **options)

    def get(self, key, default=None, **options):
        """
        gets the value from cache.

        if key does not exist, it returns None or the specified default value.

        :param object key: hashable key to get its value from cache.
        :param object default: value to be returned if key is not present.

        :returns: object
        """

        key_hash = hash(key)
        result = self._container.get(key_hash, default)
        if result in (None, default):
            self._miss_count = self._miss_count + 1
            return result

        if result.is_expired is True:
            self._miss_count = self._miss_count + 1
            self.remove(key_hash)
            return default

        self._hit_count = self._hit_count + 1
        result.refresh()
        self._container.move_to_end(key_hash, not self._use_lifo)
        return result.value

    @property
    def is_full(self):
        """
        gets a value indicating the cache is full.

        it returns a tuple, first item is a boolean indicating the fullness of cache.
        the second item is the number of excess items in the cache that must be removed.
        the excess value will be calculated using `clear_count` property of this handler.

        :rtype: tuple[bool, int]
        """

        if self.limit == NO_LIMIT:
            return False

        count = self.count
        is_full = False
        excess = 0
        if count >= self.limit:
            is_full = True
            excess = count - self.limit + self._clear_count + 1

        return is_full, excess

    @property
    def timeout(self):
        """
        gets timeout value for this handler items in milliseconds.

        :rtype: int
        """

        return self._timeout

    @property
    def limit(self):
        """
        gets the size limit of this handler.

        :rtype: int
        """

        return self._limit

    @property
    def hit_count(self):
        """
        gets the hit count for this handler.

        :rtype: int
        """

        return self._hit_count

    @property
    def miss_count(self):
        """
        gets the miss count for this handler.

        :rtype: int
        """

        return self._miss_count

    @property
    def use_lifo(self):
        """
        gets the use lifo for this handler.

        :rtype: bool
        """

        return self._use_lifo

    @property
    def clear_count(self):
        """
        gets the clear count for this handler.

        :rtype: int
        """

        return self._clear_count

    @property
    def stats(self):
        """
        get the statistic info about cached items.

        :returns: dict(int count: items count,
                       int hit: hit count,
                       int miss: miss count,
                       str hit_ratio: hit ratio,
                       int limit: items count limit,
                       int timeout: items default timeout,
                       datetime last_cleared_time: last cleared time,
                       bool use_lifo: use lifo order,
                       int clear_count: clear count,
                       bool consider_user: consider user in cache key)
        :rtype: dict
        """

        base_stats = super().stats
        hit_ratio = self._get_hit_ratio()
        hit_ratio = '{:0.1f}%'.format(hit_ratio)
        stats = dict(hit=self.hit_count,
                     miss=self.miss_count,
                     hit_ratio=hit_ratio,
                     limit=self.limit,
                     timeout=self.timeout,
                     use_lifo=self.use_lifo,
                     clear_count=self.clear_count,
                     consider_user=self.consider_user)

        return base_stats.update(stats)
