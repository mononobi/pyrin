# -*- coding: utf-8 -*-
"""
babel manager module.
"""

from pyrin.cli.mixin import CLIMixin
from pyrin.core.context import Manager
from pyrin.globalization.locale.babel.interface import BabelCLIHandlerBase


class BabelManager(Manager, CLIMixin):
    """
    babel manager class.
    """

    _cli_handler_type = BabelCLIHandlerBase
