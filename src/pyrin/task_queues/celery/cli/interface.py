# -*- coding: utf-8 -*-
"""
celery cli interface module.
"""

from pyrin.cli.base import CLIHandlerBase
from pyrin.cli.params import CLIParamBase
from pyrin.core.globals import LIST_TYPES


class CeleryCLIParamBase(CLIParamBase):
    """
    celery cli param base class.

    all celery cli param classes must be subclassed from this.
    """

    def _convert_result(self, value):
        """
        converts the given value to required type.

        celery command line arguments must be all strings.

        :param list[object] | object value: value to be converted.

        :rtype: list[object] | object
        """

        if value is not None and not isinstance(value, str):
            if isinstance(value, LIST_TYPES):
                original_type = type(value)
                converted_results = []
                for item in value:
                    if item is not None and not isinstance(item, str):
                        converted_results.append(str(item))
                    else:
                        converted_results.append(item)
                return original_type(converted_results)

            else:
                return str(value)

        return value


class CeleryCLIHandlerBase(CLIHandlerBase):
    """
    celery cli handler base class.

    all celery cli handlers must be subclassed from this.
    """

    def __init__(self, name):
        """
        initializes an instance of CeleryCLIHandlerBase.

        :param str name: the handler name that should be registered
                         with. this name must be the exact name that
                         this handler must emmit to cli.
        """

        super().__init__(name)

    def _get_common_cli_options(self):
        """
        gets the list of common cli options.

        :rtype: list
        """

        return ['celery', '-A', 'cli:celery_app']
