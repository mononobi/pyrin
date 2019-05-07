# -*- coding: utf-8 -*-
"""
users api module.
"""

from bshop.core.context import DTO
from bshop.core import _get_app
from bshop.core.logging.decorators import audit

app = _get_app()


@app.route('/hello', methods=['GET'])
def say_hello(some_date, some_time, some_datetime, **options):
    # t0 = datetime.now()
    # ic = DTO(dic={'work': ['2011.03.02','1998/10/23', '1970.04.04']}, code=100, name='al', user_name='mononobi', age=23, date='2002-12-25', items=[{'date': '2010/12/14'}, {'date': '2015/11/03'}])
    # c = options.get('code', None)
    # a = options.get('age', None)
    # y = int(options.get('year', 0))
    # t1 = datetime.now()
    # nd = deserializer_services.deserialize(ic)
    # t2 = datetime.now()
    # print('API ROUTE')
    return DTO(some_date=some_date, some_time=some_time, some_datetime=some_datetime, **options)
    # return None
    #return DTO(code=c, name='لبیس', user_name='mononobi', age=a, year=y)

@app.route('/hello2', methods=['GET'], host=True)
def say_hello1(some_date, some_time, some_datetime, **options):
    # t0 = datetime.now()
    # ic = DTO(dic={'work': ['2011.03.02','1998/10/23', '1970.04.04']}, code=100, name='al', user_name='mononobi', age=23, date='2002-12-25', items=[{'date': '2010/12/14'}, {'date': '2015/11/03'}])
    # c = options.get('code', None)
    # a = options.get('age', None)
    # y = int(options.get('year', 0))
    # t1 = datetime.now()
    # nd = deserializer_services.deserialize(ic)
    # t2 = datetime.now()
    # print('API ROUTE')
    return DTO(some_date=some_date, some_time=some_time, some_datetime=some_datetime, **options)
    # return None
    #return DTO(code=c, name='لبیس', user_name='mononobi', age=a, year=y)



# {'work': ['2011.03.02','1998/10/23', '1970.04.04']}
# date='2002-12-25'
# items=[{'date': '2010/12/14'}, {'date': '2015/11/03'}]
#
#