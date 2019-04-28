# -*- coding: utf-8 -*-
"""
Main entry point for bshop server.
It should be run without debug flag in production environments.
"""

from bshop.core.application import app

app.run(use_reloader=False)
