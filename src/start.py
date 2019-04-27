# -*- coding: utf-8 -*-
"""
Main entry point for bshop server.
It should be run without debug flag in production environments.
"""


def method(**kwargs):
    print(type(kwargs))
    for v in kwargs.values():
        print(v)


d = {'name': 'ali', 'age': 30}


def method_two(**dic):
    di = {'NAM': 'HASAN', 'AGE': 45}
    for k in dic.keys():
        dic[k] = di
        di = None
    di = None

    print(dic)


from bshop.core.application import app
from  bshop.core.api.deserializers.decorators import register
from bshop.core.application.services import add_context
# from bshop import settings
from bshop.core.context import DynamicObject
# from bshop.core.application.base import Application
from flask import Flask, jsonify

#register(name=3)
# app = Application('bshop')
# app.config.from_object(settings)
# @api.route('/hello')
# class HelloWorld(Resource):
#     @api.route('/hello', methods=['GET'])
#     def get(self):
#         return DynamicObject(id=1000, name='test', cars=['bmw', 'mercedes', 'pride']), 300

# @app.route('/', methods=['GET'])
# def say_hello():
#     s = app_config.AppConfig.APP_CONFIG_FILE
#     # raise Exception('error')
#     return make_response(jsonify(DynamicObject(id=1000,
#                                                name='test',
#                                                cars=['bmw',
#                                                      'mercedes',
#                                                      'pride'])), 202)

def accepted_type():
    """
    Gets the accepted type for this deserializer
    which could deserialize values from this type.

    :rtype: type
    """

    return bool

# @app.route('/', methods=['GET'])
# def say_hello2(**kwargs):
#     return jsonify(DynamicObject(id=1000,
#                                  name='test',
#                                  cars=['bmw',
#                                        'mercedes',
#                                        'pride']))


if __name__ == '__main__':
    #method_two(**d)
    #app.run(use_reloader=False)

    print(accepted_type()('dsfdfs'))

