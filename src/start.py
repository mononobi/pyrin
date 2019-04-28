# -*- coding: utf-8 -*-
"""
Main entry point for bshop server.
It should be run without debug flag in production environments.
"""

from bshop.core.application.base import Application

app = Application('bshop')
app.run(use_reloader=False)
