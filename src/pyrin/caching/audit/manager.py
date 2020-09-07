# -*- coding: utf-8 -*-
"""
caching audit manager module.
"""

import traceback

import pyrin.caching.services as caching_services

from pyrin.audit.enumerations import InspectionStatusEnum
from pyrin.caching.audit import CachingAuditPackage
from pyrin.core.structs import Manager


class CachingAuditManager(Manager):
    """
    caching audit manager class.
    """

    package_class = CachingAuditPackage

    def inspect(self, **options):
        """
        inspects the status of available caches.

        it returns a tuple of two values. first value is a dict containing the inspection
        data. and the second value is a bool value indicating that inspection has been
        succeeded or failed.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :rtype: tuple[dict, bool]
        """

        all_caches = caching_services.get_cache_names()
        all_succeeded = True
        data = {}
        data.update(all_caches=all_caches)

        for name in all_caches:
            inspection_data, succeeded = self._test_cache(name, **options)
            inspection_data.update(stats=caching_services.get_stats(name))
            if succeeded is False:
                all_succeeded = False
            data[name] = inspection_data

        return data, all_succeeded

    def _test_cache(self, name, **options):
        """
        tests that given cache is ready.

        it returns a tuple of two values. first value is a dict containing the inspection
        data. and the second value is a bool value indicating that inspection has been
        succeeded or failed.

        :param str name: cache name.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :rtype: tuple[dict, bool]
        """

        include_traceback = options.get('traceback', True)
        data = {}
        succeeded = True
        try:
            key = 'audit.test'
            value = [1, 2, 3]
            caching_services.set(name, key, value)
            result = caching_services.get(name, key)
            caching_services.remove(name, key)

            if result != value:
                raise Exception('Result for key [{key}] did not returned '
                                'correctly from cache.'.format(key=key))

            data.update(status=InspectionStatusEnum.OK)
        except Exception as error:
            succeeded = False
            data.update(status=InspectionStatusEnum.FAILED,
                        error=str(error))
            if include_traceback is not False:
                data.update(traceback=traceback.format_exc())

        return data, succeeded
