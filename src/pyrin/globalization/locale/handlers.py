# -*- coding: utf-8 -*-
"""
locale handlers module.
"""

import pyrin.globalization.locale.services as locale_services


locale_services.set_locale_selector(locale_services.get_current_locale)
locale_services.set_timezone_selector(locale_services.get_current_timezone)
