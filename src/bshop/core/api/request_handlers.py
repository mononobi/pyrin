# -*- coding: utf-8 -*-
"""
API request handlers module.
"""

from flask import request
from bshop.core.application import app
from bshop.core.context import DynamicObject


@app.before_request
def before_request():
    """
    Before request handler.
    This method will be executed before every request.
    """

    params = DynamicObject(**(request.view_args or {}),
                           **(request.get_json(force=True, silent=True) or {}),
                           query_params=request.args,
                           files=request.files)

    request.view_args = params
