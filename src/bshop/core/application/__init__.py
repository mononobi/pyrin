# -*- coding: utf-8 -*-
"""
Application package.
"""

import bshop.core.application.manager

app = manager.create_application(__name__.split('.')[0])
