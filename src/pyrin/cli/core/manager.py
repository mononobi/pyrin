# -*- coding: utf-8 -*-
"""
cli core manager module.
"""

from pyrin.cli.core import CLICorePackage
from pyrin.cli.core.exceptions import CLICoreTemplateHandlerNotFoundError
from pyrin.cli.core.template.handlers import ScriptsTemplateHandler, ApplicationTemplateHandler
from pyrin.core.structs import Manager, DTO


class CLICoreManager(Manager):
    """
    cli core manager class.
    """

    package_class = CLICorePackage

    def __init__(self):
        """
        initializes an instance of CLICoreManager.
        """

        super().__init__()

        scripts_handler = ScriptsTemplateHandler()
        application_handler = ApplicationTemplateHandler()
        scripts_handler.set_next(application_handler)

        self._handlers = DTO(project=[scripts_handler, application_handler])

    def create(self, handler_name):
        """
        creates the required templates using relevant handlers.

        :param str handler_name: handler name to be used.

        :raises CLICoreTemplateHandlerNotFoundError: cli core template handler not found error.
        """

        handler = self._get_handler(handler_name)
        handler.create()

    def _get_handler(self, name):
        """
        gets the requested handler with given name.

        :param str name: handler name to be get.

        :raises CLICoreTemplateHandlerNotFoundError: cli core template handler not found error.

        :rtype: ProjectStructureTemplateHandlerBase
        """

        if name not in self._handlers:
            raise CLICoreTemplateHandlerNotFoundError('Command [{name}] is not valid. '
                                                      'available commands: {commands}.'
                                                      .format(name=name,
                                                              commands=
                                                              list(self._handlers.keys())))

        return self._handlers[name][0]
