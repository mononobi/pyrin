# -*- coding: utf-8 -*-
"""
validator auto hooks module.
"""

import pyrin.validator.auto.services as validator_auto_services

from pyrin.core.structs import Hook
from pyrin.database.model.decorators import model_hook
from pyrin.database.model.hooks import ModelHookBase
from pyrin.utils.custom_print import print_info


class AutoValidatorHookBase(Hook):
    """
    auto validator hook base class.
    """

    def after_auto_validators_registered(self):
        """
        this method will be called after all application auto validators have been registered.
        """
        pass


@model_hook()
class ModelHook(ModelHookBase):
    """
    model hook class.
    """

    def after_entities_collected(self):
        """
        this method will be called after all application entities have been collected.
        """

        count = validator_auto_services.register_auto_validators()
        if count > 0:
            print_info('Total of [{count}] auto validators registered.'.format(count=count))
