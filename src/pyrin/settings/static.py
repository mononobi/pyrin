# -*- coding: utf-8 -*-
"""
settings static module.
these settings are intended for values used inside some classes,
to be available before server startup.
"""

# default response status code.
DEFAULT_STATUS_CODE = 200

# default application encoding.
APPLICATION_ENCODING = 'utf-8'

# this value will be used to register default components that does not belong
# to any custom implementation. any other custom implementation that needs to be
# exposed through services, should provide it's own relevant key.
# example for COMPONENT_ID:
# (__name__, DEFAULT_COMPONENT_KEY) -> default
# (__name__, 4) -> custom
DEFAULT_COMPONENT_KEY = 0
