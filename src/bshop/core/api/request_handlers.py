# -*- coding: utf-8 -*-
"""
request handlers module.
"""

from flask import request

from bshop.core import _get_app
from bshop.core.context import DTO

app = _get_app()


@app.before_request
def request_input_mapper():
    """
    before request handler for mapping input params into view function.
    this method will be executed before every request.
    """

    request.view_args = DTO(**(request.view_args or {}),
                            **(request.get_json(force=True, silent=True) or {}),
                            query_params=request.args,
                            files=request.files)


