# -*- coding: utf-8 -*-
"""
datetime manager module.
"""

from datetime import datetime

import pytz

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject


class DateTimeManager(CoreObject):
    """
    datetime manager class.
    """

    def __init__(self, **options):
        """
        initializes an instance of DateTimeManager.
        """

        CoreObject.__init__(self)

        default_timezone = config_services.get('globalization', 'datetime', 'default_timezone')
        self.__current_timezone = pytz.timezone(default_timezone)

    def now(self):
        """
        gets current datetime based on application current timezone.

        :rtype: datetime
        """

        return datetime.now(self.get_current_timezone())

    def get_current_timezone(self):
        """
        gets the application current timezone.

        :rtype: tzinfo
        """

        return self.__current_timezone
