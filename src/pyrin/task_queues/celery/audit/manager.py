# -*- coding: utf-8 -*-
"""
celery audit manager module.
"""

import traceback

from pyrin.core.structs import Manager
from pyrin.audit.enumerations import InspectionStatusEnum
from pyrin.task_queues.celery.audit import CeleryAuditPackage
from pyrin.task_queues.celery.audit.tasks import audit_task


class CeleryAuditManager(Manager):
    """
    celery audit manager class.
    """

    package_class = CeleryAuditPackage

    def __init__(self):
        """
        initializes an instance of CeleryAuditManager.
        """

        super().__init__()

    def inspect(self, **options):
        """
        inspects the status of celery.

        it returns a tuple of two values. first value is a dict containing the inspection
        data. and the second value is a bool value indicating that inspection has been
        succeeded or failed.

        :keyword bool traceback: specifies that on failure report, it must include
                                 the traceback of errors.
                                 defaults to True if not provided.

        :rtype: tuple[dict, bool]
        """

        include_traceback = options.get('traceback', True)
        data = {}
        succeeded = True
        try:
            audit_task.delay(suppress=False)
            data.update(status=InspectionStatusEnum.OK)
        except Exception as error:
            succeeded = False
            data.update(status=InspectionStatusEnum.FAILED,
                        error=str(error))
            if include_traceback is not False:
                data.update(traceback=traceback.format_exc())

        return data, succeeded

    def perform_job(self):
        """
        performs a dummy job.

        this method is implemented to be called by `audit_task` to check celery.
        """
        pass
