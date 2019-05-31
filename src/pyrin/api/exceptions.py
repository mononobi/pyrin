# -*- coding: utf-8 -*-
"""
api exceptions module.
"""

from werkzeug.exceptions import HTTPException

from pyrin.core.exceptions import CoreException


class CoreHTTPException(HTTPException, CoreException):
    """
    base class for all application http exceptions.
    """

    def __init__(self, *args):
        super(CoreHTTPException, self).__init__(*args)
