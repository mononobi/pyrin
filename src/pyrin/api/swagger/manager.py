# -*- coding: utf-8 -*-
"""
swagger manager module.
"""

import pyrin.configuration.services as config_services

from pyrin.core.structs import Manager, Context
from pyrin.utils.custom_print import print_warning
from pyrin.api.swagger.interface import AbstractTag
from pyrin.api.swagger.base import ExtendedSwagger
from pyrin.application.services import get_current_app
from pyrin.api.swagger import SwaggerPackage
from pyrin.api.swagger.exceptions import InvalidTagTypeError, DuplicatedTagError


class SwaggerManager(Manager):
    """
    swagger manager class.
    """

    package_class = SwaggerPackage

    def __init__(self):
        """
        initializes an instance of SwaggerManager.
        """

        super().__init__()

        # a dict containing all registered tags in the form of:
        # {str name: AbstractTag instance}
        self._tags = Context()

        self._swagger = None
        if self._is_enabled() is True:
            self._swagger = ExtendedSwagger(get_current_app(),
                                            config=self._get_configs(),
                                            merge=True)

    def _is_enabled(self):
        """
        gets a value indicating that swagger ui is enabled.

        :rtype: bool
        """

        return config_services.get_active('swagger', 'enabled')

    def _is_disabled_tag(self, tag):
        """
        gets a value indicating that given tag is disabled.

        :param str tag: tag name to be checked.

        :rtype: bool
        """

        disabled_tags = config_services.get_active('swagger', 'disabled_tags')
        return tag in disabled_tags

    def _get_custom_tags(self):
        """
        gets a dict of all custom tags.

        :rtype: dict
        """

        return config_services.get_active('swagger', 'custom_tags')

    def _get_configs(self):
        """
        gets configuration from `swagger` config store.

        :rtype: dict
        """

        return config_services.get_active_section('swagger')

    def register_tag(self, instance, **options):
        """
        registers a new tag or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a tag which is already registered.

        :param AbstractTag instance: tag to be registered.
                                     it must be an instance of AbstractTag.

        :keyword bool replace: specifies that if there is another registered
                               tag with the same name, replace it with the
                               new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidTagTypeError: invalid tag type error.
        :raises DuplicatedTagError: duplicated tag error.
        """

        if not isinstance(instance, AbstractTag):
            raise InvalidTagTypeError('Input parameter [{instance}] is '
                                      'not an instance of [{base}].'
                                      .format(instance=instance,
                                              base=AbstractTag))

        if instance.name in self._tags:
            old_instance = self._tags.get(instance.name)
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedTagError('There is another registered tag '
                                         '[{old}] with name [{name}] but "replace" '
                                         'option is not set, so tag [{instance}] '
                                         'could not be registered.'
                                         .format(old=old_instance,
                                                 name=instance.name,
                                                 instance=instance))

            print_warning('Tag [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._tags[instance.name] = instance

    def get_tags(self, rule, method, **options):
        """
        gets the valid tags for given rule.

        :param pyrin.api.router.handlers.base.RouteBase rule: rule instance to be processed.
        :param str method: http method name.

        :rtype: list[str]
        """

        tags = []
        for name, item in self._tags.items():
            if not self._is_disabled_tag(name):
                if item.is_accepted(rule, method):
                    tags.append(item.tag)

        custom_tags = self._get_custom_tags()
        for name, value in custom_tags.items():
            if not self._is_disabled_tag(name):
                if rule.rule.startswith(value):
                    tags.append(name)

        return list(set(tags))
