# -*- coding: utf-8 -*-
"""
request handlers module.
"""

from flask import request

from bshop.core.application.decorators import before_request_handler
from bshop.core.context import DTO


@before_request_handler()
def request_param_mapper():
    """
    before request handler for mapping input params into view arguments.
    this method will be executed before every request.
    """

    request.view_args = DTO(**(request.view_args or {}),
                            **(request.get_json(force=True, silent=True) or {}),
                            query_params=request.args,
                            files=request.files)
