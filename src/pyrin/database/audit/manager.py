# -*- coding: utf-8 -*-
"""
database audit manager module.
"""

import traceback

import pyrin.database.services as database_services

from pyrin.audit.enumerations import InspectionStatusEnum
from pyrin.database.audit import DatabaseAuditPackage
from pyrin.core.structs import Manager
from pyrin.database.services import get_current_store


class DatabaseAuditManager(Manager):
    """
    database audit manager class.
    """

    package_class = DatabaseAuditPackage

    def inspect(self, **options):
        """
        inspects the status of available databases.

        it returns a tuple of two values. first value is a dict containing the inspection
        data. and the second value is a bool value indicating that inspection has been
        succeeded or failed.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :keyword bool raise_error: specifies that it must raise error
                                   if any of registered audits failed
                                   instead of returning a failure response.
                                   defaults to False if not provided.

        :rtype: tuple[dict, bool]
        """

        all_databases = database_services.get_all_database_names()
        default_database = database_services.get_default_database_name()
        all_succeeded = True
        data = {}

        for item in all_databases:
            name = item
            if item == default_database:
                name = None
            inspection_data, succeeded = self._test_database(name, **options)
            if succeeded is False:
                all_succeeded = False
            data[item] = inspection_data

        return data, all_succeeded

    def _test_database(self, bind_name=None, **options):
        """
        tests that given bind name database is ready.

        it returns a tuple of two values. first value is a dict containing the inspection
        data. and the second value is a bool value indicating that inspection has been
        succeeded or failed.

        :param str bind_name: database bind name from `database.binds` config store.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :keyword bool raise_error: specifies that it must raise error
                                   if any of registered audits failed
                                   instead of returning a failure response.
                                   defaults to False if not provided.

        :rtype: tuple[dict, bool]
        """

        raise_error = options.get('raise_error', False)
        include_traceback = options.get('traceback', True)
        store = get_current_store()
        data = {}
        succeeded = True
        try:
            store.execute('select 1', bind_name=bind_name)
            data.update(status=InspectionStatusEnum.OK)
        except Exception as error:
            if raise_error is True:
                raise

            succeeded = False
            data.update(status=InspectionStatusEnum.FAILED,
                        error=str(error))
            if include_traceback is not False:
                data.update(traceback=traceback.format_exc())

        return data, succeeded
