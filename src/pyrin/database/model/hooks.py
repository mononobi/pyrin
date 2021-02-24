# -*- coding: utf-8 -*-
"""
model hooks module.
"""

import pyrin.database.model.services as model_services

from pyrin.core.structs import Hook
from pyrin.packaging.decorators import packaging_hook
from pyrin.packaging.hooks import PackagingHookBase
from pyrin.utils.custom_print import print_info


class ModelHookBase(Hook):
    """
    model hook base class.
    """

    def after_entities_collected(self):
        """
        this method will be called after all application entities have been collected.
        """
        pass


@packaging_hook()
class PackagingHook(PackagingHookBase):
    """
    packaging hook class.
    """

    def after_packages_loaded(self):
        """
        this method will be called after all application packages have been loaded.
        """

        count = model_services.collect_entities()
        if count > 0:
            print_info('Total of [{count}] entities collected.'.format(count=count))
