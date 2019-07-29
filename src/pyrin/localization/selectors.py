# -*- coding: utf-8 -*-
"""
localization selectors module.
"""

import pyrin.localization.services as localization_services


localization_services.set_locale_selector(localization_services.get_current_locale)
localization_services.set_timezone_selector(localization_services.get_current_timezone)
