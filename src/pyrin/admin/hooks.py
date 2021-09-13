# -*- coding: utf-8 -*-
"""
admin hooks module.
"""

import pyrin.admin.services as admin_services

from pyrin.utils.custom_print import print_info
from pyrin.validator.auto.hooks import AutoValidatorHookBase
from pyrin.validator.auto.decorators import auto_validator_hook


@auto_validator_hook()
class AutoValidatorHook(AutoValidatorHookBase):
    """
    auto validator hook class.
    """

    def after_auto_validators_registered(self):
        """
        this method will be called after all application auto validators have been registered.
        """

        count = admin_services.populate_caches()
        admin_services.populate_main_metadata()
        if count > 0:
            print_info('Total of [{count}] admin pages registered.'.format(count=count))
