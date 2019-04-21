# -*- coding: utf-8 -*-
"""
Application implementation module.
"""

from bshop.core.application.base import Application
from bshop import settings
# from bshop.core import packaging
# from bshop import test_api

from datetime import datetime


def create_application(import_name, **kwargs):
    """
    Creates and configures application.

    :param str import_name: the name of the application package.

    :rtype: Application
    """

    app = Application(import_name, **kwargs)
    app.config.from_object(settings)

    print(datetime.now())

    return app
