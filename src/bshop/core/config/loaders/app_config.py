# -*- coding: utf-8 -*-
"""
App configuration file loader.
"""

from bshop.core.base import ObjectBase


class AppConfig(ObjectBase):
    """
    App configuration file loader
    """

    APP_CONFIG_FILE = "settings/app.config"

    def __init__(self):
        ObjectBase.__init__(self)

    def load(self):
        """
        Loads app configuration file.

        :rtype: dict
        """

        pass
