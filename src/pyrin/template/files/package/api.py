# -*- coding: utf-8 -*-
"""
PACKAGE_NAME api module.
"""

from pyrin.api.router.decorators import api
from pyrin.core.enumerations import HTTPMethodEnum

import PACKAGE_FULL_NAME.services as PACKAGE_NAME_services


# Usage:
# you could implement different api functions here and call corresponding service method this way:
# return PACKAGE_NAME_services.method_name(*arg, **kwargs)
