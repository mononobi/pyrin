# -*- coding: utf-8 -*-
"""
Main entry point for bshop server.
It should be run without debug flag in production environments.
"""

from bshop.core.context import DynamicObject
from bshop.core.application import app
from bshop.core.packaging import manager as packaging_manager

# @api.route('/hello')
# class HelloWorld(Resource):
#     @api.route('/hello', methods=['GET'])
#     def get(self):
#         return DynamicObject(id=1000, name='test', cars=['bmw', 'mercedes', 'pride']), 300
packaging_manager.load_packages()

# @app.route('/', methods=['GET'])
# def say_hello():
#     s = app_config.AppConfig.APP_CONFIG_FILE
#     # raise Exception('error')
#     return make_response(jsonify(DynamicObject(id=1000,
#                                                name='test',
#                                                cars=['bmw',
#                                                      'mercedes',
#                                                      'pride'])), 202)

# @app.route('/hello', methods=['GET'])
# def say_hello():
#     #raise Exception('error')
#     return DynamicObject(id=1000,
#                          name='test',
#                          cars=['bmw',
#                                'mercedes',
#                                'pride']), 202


@app.errorhandler(Exception)
def error(exception):
    return DynamicObject(message='error occured'), 500


@app.errorhandler(500)
def error(exception):
    return DynamicObject(message='error 500'), 600


if __name__ == '__main__':
    app.run(debug=True)
