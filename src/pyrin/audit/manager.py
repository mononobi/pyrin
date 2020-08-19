# -*- coding: utf-8 -*-
"""
audit manager module.
"""

import pyrin
import pyrin.application.services as application_services
import pyrin.packaging.services as packaging_services

from pyrin.audit.exceptions import InvalidAuditHookTypeError
from pyrin.audit.hooks import AuditHookBase
from pyrin.core.mixin import HookMixin
from pyrin.core.structs import Manager
from pyrin.audit import AuditPackage


class AuditManager(Manager, HookMixin):
    """
    audit manager class.

    this class provides some hooks to let different packages expose some audit services.
    it could be helpful to check system stability and status after a new deployment.
    """

    package_class = AuditPackage
    hook_type = AuditHookBase
    invalid_hook_type_error = InvalidAuditHookTypeError

    def _inspect(self, **options):
        """
        this method will call `inspect` method of all registered hooks.

        :rtype: dict
        """

        data = {}
        for hook in self._get_hooks():
            try:
                result = hook.inspect(**options)
                data[hook.audit_name] = result
            except Exception as error:
                data[hook.audit_name] = dict(status='Failed', error=str(error))

        return data

    def inspect(self, **options):
        """
        inspects all registered packages and gets inspection data.

        :keyword bool verbose: specifies that verbose info should be returned.
                               it includes the name and count of loaded packages.
                               defaults to False if not provided.

        :rtype: dict
        """

        verbose = options.get('verbose', False)
        data = self._inspect(**options)
        data.update(application=self.get_application_info(**options),
                    framework=self.get_framework_info(**options))

        if verbose is True:
            packages = packaging_services.get_loaded_packages()
            data.update(packages=packages,
                        packages_count=len(packages))

        packages_info = self._inspect(**options)
        data.update(packages_info)

        return data

    def get_application_info(self, **options):
        """
        gets info of current application.

        :rtype: dict
        """

        data = {}
        data.update(name=application_services.get_application_name())
        return data

    def get_framework_info(self, **options):
        """
        gets info of current framework.

        :rtype: dict
        """

        data = {}
        data.update(name='pyrin', version=pyrin.__version__)
        return data
