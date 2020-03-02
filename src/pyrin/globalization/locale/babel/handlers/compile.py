# -*- coding: utf-8 -*-
"""
babel handlers compile module.
"""

from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import DomainParamMixin, \
    InputFileParamMixin, LocaleParamMixin, UseFuzzyParamMixin, StatisticsParamMixin, \
    DirectoryParamMixin


@babel_cli_handler()
class CompileCLIHandler(DomainParamMixin, DirectoryParamMixin,
                        InputFileParamMixin, LocaleParamMixin,
                        UseFuzzyParamMixin, StatisticsParamMixin):
    """
    compile cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of CompileCLIHandler.
        """

        super().__init__('compile')
