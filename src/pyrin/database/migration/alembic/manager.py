# -*- coding: utf-8 -*-
"""
database migration alembic manager module.
"""

from pyrin.core.context import Manager, DTO
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase
from pyrin.utils.custom_print import print_warning
from pyrin.database.migration.alembic.exceptions import InvalidAlembicCLIHandlerTypeError, \
    DuplicatedAlembicCLIHandlerError, AlembicCLIHandlerNotFoundError


class DatabaseMigrationAlembicManager(Manager):
    """
    database migration alembic manager class.
    """

    def __init__(self):
        """
        initializes an instance of DatabaseMigrationAlembicManager.
        """

        super().__init__()

        # a dictionary containing cli handlers
        # for different alembic commands.
        # in the form of: {str command name: CLIHandlerBase handler}
        self._cli_handlers = DTO()

    def register_cli_handler(self, instance, **options):
        """
        registers a new alembic cli handler or replaces the existing one
        if `replace=True` is provided. otherwise, it raises an error
        on adding a cli handler which is already registered.

        :param AlembicCLIHandlerBase instance: alembic cli handler to be registered.
                                               it must be an instance of
                                               AlembicCLIHandlerBase.

        :keyword bool replace: specifies that if there is another registered
                               cli handler with the same name, replace it
                               with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidAlembicCLIHandlerTypeError: invalid alembic cli handler type error.
        :raises DuplicatedAlembicCLIHandlerError: duplicated alembic cli handler error.
        """

        if not isinstance(instance, AlembicCLIHandlerBase):
            raise InvalidAlembicCLIHandlerTypeError('Input parameter [{instance}] is '
                                                    'not an instance of AlembicCLIHandlerBase.'
                                                    .format(instance=str(instance)))

        if instance.get_name() in self._cli_handlers:
            old_instance = self._cli_handlers.get(instance.get_name())
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedAlembicCLIHandlerError('There is another registered '
                                                       'cli handler with name [{name}] '
                                                       'but "replace" option is not set, so '
                                                       'cli handler [{instance}] could not '
                                                       'be registered.'
                                                       .format(name=instance.get_name(),
                                                               instance=str(instance)))

            print_warning('Alembic cli handler [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance),
                                  new_instance=str(instance)))

        self._cli_handlers[instance.get_name()] = instance

    def _get_cli_handler(self, name):
        """
        gets an alembic cli handler with the given name.
        if not available, it raises an error.

        :param str name: alembic cli handler name to get its instance.

        :raises AlembicCLIHandlerNotFoundError: alembic cli handler not found error.

        :rtype: AlembicCLIHandlerBase
        """

        if name not in self._cli_handlers:
            raise AlembicCLIHandlerNotFoundError('Alembic cli handler with name '
                                                 '[{name}] not found.'
                                                 .format(name=name))

        return self._cli_handlers[name]

    def execute(self, name, **options):
        """
        executes the handler with the given name with given inputs.

        :param str name: handler name tobe executed.

        :raises AlembicCLIHandlerNotFoundError: alembic cli handler not found error.
        """

        handler = self._get_cli_handler(name)
        handler.execute(**options)
