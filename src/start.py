# -*- coding: utf-8 -*-
"""
main entry point for bshop server.
it should be run without debug flag in production environments.
"""

from bshop.core.application.base import Application

app = Application('bshop')
app.run(use_reloader=False)
