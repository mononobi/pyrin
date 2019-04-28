# -*- coding: utf-8 -*-
"""
Users exposed api module.
"""

from datetime import datetime

import bshop.core.api.deserializer.services as deserializer_services
from bshop.core.context import DTO
from bshop.core import _get_app

app = _get_app()

@app.route('/hello', methods=['GET'])
def say_hello(dic, date, items, **options):

    # t0 = datetime.now()
    # ic = DTO(dic={'work': ['2011.03.02','1998/10/23', '1970.04.04']}, code=100, name='al', user_name='mononobi', age=23, date='2002-12-25', items=[{'date': '2010/12/14'}, {'date': '2015/11/03'}])
    # c = options.get('code', None)
    # a = options.get('age', None)
    # y = int(options.get('year', 0))
    # t1 = datetime.now()
    # nd = deserializer_services.deserialize(ic)
    # t2 = datetime.now()
    # print('API ROUTE')
    return DTO(items=items, date=date, dic=dic, **options)
    #return DTO(code=c, name='لبیس', user_name='mononobi', age=a, year=y)



# {'work': ['2011.03.02','1998/10/23', '1970.04.04']}
# date='2002-12-25'
# items=[{'date': '2010/12/14'}, {'date': '2015/11/03'}]
#
#