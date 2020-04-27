# -*- coding: utf-8 -*-
"""
mimetype exceptions module.
"""

from pyrin.core.exceptions import CoreException


class MIMETypeManagerException(CoreException):
    """
    mimetype manager exception.
    """
    pass


class InvalidMIMETypeHandlerTypeError(MIMETypeManagerException):
    """
    invalid mimetype handler type error.
    """
    pass


class DuplicatedMIMETypeHandlerError(MIMETypeManagerException):
    """
    duplicated mimetype handler error.
    """
    pass
