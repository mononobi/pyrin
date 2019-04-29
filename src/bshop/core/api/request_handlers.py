# -*- coding: utf-8 -*-
"""
request handlers module.
"""

from flask import request

import bshop.core.api.deserializer.services as deserializer_services

from bshop.core import _get_app
from bshop.core.context import DTO

app = _get_app()


@app.before_request
def request_deserializer():
    """
    before request handlers for deserialization.
    this method will be executed before every request.
    """

    params = DTO(**(request.view_args or {}),
                 **(request.get_json(force=True, silent=True) or {}),
                 query_params=request.args,
                 files=request.files)

    deserialized_value = deserializer_services.deserialize(params)
    if deserialized_value is not None:
        request.view_args = deserialized_value
    else:
        request.view_args = params

