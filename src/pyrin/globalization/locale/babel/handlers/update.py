# -*- coding: utf-8 -*-
"""
babel handlers update module.
"""

from pyrin.globalization.locale.babel.decorators import babel_cli_handler
from pyrin.globalization.locale.babel.handlers.params import DomainParamMixin, \
    InputFileParamMixin, OutputDirectoryParamMixin, OmitHeaderParamMixin, LocaleParamMixin, \
    WidthParamMixin, NoWrapParamMixin, IgnoreObsoleteParamMixin, NoFuzzyMatchingParamMixin, \
    UpdateHeaderCommentParamMixin, PreviousParamMixin


@babel_cli_handler()
class UpdateCLIHandler(DomainParamMixin, InputFileParamMixin,
                       OutputDirectoryParamMixin, OmitHeaderParamMixin,
                       LocaleParamMixin, WidthParamMixin, NoWrapParamMixin,
                       IgnoreObsoleteParamMixin, NoFuzzyMatchingParamMixin,
                       UpdateHeaderCommentParamMixin, PreviousParamMixin):
    """
    update cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of UpdateCLIHandler.
        """

        super().__init__('update')
