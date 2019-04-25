# -*- coding: utf-8 -*-
"""
"""

from bshop import app
from bshop.core.context import DynamicObject


@app.route('/', methods=['GET'])
def say_hello(**options):

    c = options.get('code', None)
    a = options.get('age', None)
    y = int(options.get('year', 0))
    return DynamicObject(code=c, name='لبیس', user_name='mononobi', age=a, year=y)
