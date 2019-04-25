# -*- coding: utf-8 -*-
"""
Packaging services.
"""

from bshop.core.packaging import manager


def load_components():
    """
    Loads required packages and modules for application startup.
    """

    manager.load_components()
