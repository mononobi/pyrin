# -*- coding: utf-8 -*-
"""
Users exposed api module.
"""

from bshop.core.context import DynamicObject
from bshop.core.application import app


@app.route('/hello', methods=['GET'])
def say_hello(**options):
    raise AttributeError('attr you')
    c = options.get('code', None)
    a = options.get('age', None)
    y = int(options.get('year', 0))
    print('API ROUTE')
    return DynamicObject(code=c, name='لبیس', user_name='mononobi', age=a, year=y)
