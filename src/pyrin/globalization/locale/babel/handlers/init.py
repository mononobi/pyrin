# -*- coding: utf-8 -*-
"""
babel handlers init module.
"""

from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import DomainParamMixin, \
    InputFileParamMixin, OutputDirectoryParamMixin, LocaleParamMixin, \
    WidthParamMixin, NoWrapParamMixin


@babel_cli_handler()
class InitCLIHandler(DomainParamMixin, InputFileParamMixin,
                     OutputDirectoryParamMixin, LocaleParamMixin,
                     WidthParamMixin, NoWrapParamMixin):
    """
    init cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of InitCLIHandler.
        """

        super().__init__('init')
