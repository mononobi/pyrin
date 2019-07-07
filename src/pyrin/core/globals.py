# -*- coding: utf-8 -*-
"""
core globals module.
"""

from flask_babel import gettext

from pyrin.core.context import CoreObject


# this value should be used as `None`, where the `None` itself has a meaning.
NULL = CoreObject()

# this method should be used for localizable strings.
_ = gettext
