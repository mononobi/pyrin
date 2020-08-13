# -*- coding: utf-8 -*-
"""
template manager module.
"""

from pyrin.template import TemplatePackage
from pyrin.template.interface import AbstractTemplateHandler
from pyrin.utils.custom_print import print_warning
from pyrin.core.structs import Manager, DTO
from pyrin.template.exceptions import InvalidTemplateHandlerTypeError, \
    DuplicatedTemplateHandlerError, TemplateHandlerNotFoundError


class TemplateManager(Manager):
    """
    template manager class.
    """

    package_class = TemplatePackage

    def __init__(self):
        """
        initializes an instance of TemplateManager.
        """

        super().__init__()

        # a dictionary containing template handlers.
        # in the form of: {str handler_name: AbstractTemplateHandler handler}
        self._template_handlers = DTO()

    def register_template_handler(self, instance, **options):
        """
        registers a new template handler or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding a template handler which is already registered.

        :param AbstractTemplateHandler instance: template handler to be registered.
                                                 it must be an instance of
                                                 AbstractTemplateHandler.

        :keyword bool replace: specifies that if there is another registered
                               template handler with the same name, replace it
                               with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidTemplateHandlerTypeError: invalid template handler type error.
        :raises DuplicatedTemplateHandlerError: duplicated template handler error.
        """

        if not isinstance(instance, AbstractTemplateHandler):
            raise InvalidTemplateHandlerTypeError('Input parameter [{instance}] is '
                                                  'not an instance of [{handler}].'
                                                  .format(instance=instance,
                                                          handler=AbstractTemplateHandler))

        if instance.name in self._template_handlers:
            old_instance = self._template_handlers.get(instance.name)
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedTemplateHandlerError('There is another registered '
                                                     'template handler with name [{name}] '
                                                     'but "replace" option is not set, so '
                                                     'template handler [{instance}] could '
                                                     'not be registered.'
                                                     .format(name=instance.name,
                                                             instance=instance))

            print_warning('Template handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._template_handlers[instance.name] = instance

    def _get_template_handler(self, name):
        """
        gets a template handler with the given name.

        if not available, it raises an error.

        :param str name: template handler name to get its instance.

        :raises TemplateHandlerNotFoundError: template handler not found error.

        :rtype: AbstractTemplateHandler
        """

        if name not in self._template_handlers:
            raise TemplateHandlerNotFoundError('Template handler [{name}] not found.'
                                               .format(name=name))

        return self._template_handlers[name]

    def create(self, handler_name, *args, **kwargs):
        """
        creates the template using the given template handler name.

        :param str handler_name: handler name to be used.
        :param object args: arguments that should be passed to template handler.

        :keyword object kwargs: keyword arguments that should be passed to template handler.

        :raises TemplateHandlerNotFoundError: template handler not found error.
        """

        handler = self._get_template_handler(handler_name)
        return handler.create(*args, **kwargs)
