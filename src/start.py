# -*- coding: utf-8 -*-
"""
main entry point for pyrin application.
it should be run without debug flag in production environments.
"""

from pyrin.application.base import Application

app = Application('pyrin')
app.run(use_reloader=False)
