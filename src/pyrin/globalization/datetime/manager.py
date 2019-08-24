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
        self.__active_timezone = pytz.timezone(default_timezone)

    def get_current_datetime(self):
        """
        gets current datetime in application default timezone.

        :rtype: datetime
        """

        return datetime.now(self.get_active_timezone())

    def get_normalized_datetime(self, value):
        """
        normalizes the input value to application default timezone.

        :param datetime value: value to get it's application default timezone equivalent.

        :rtype: datetime
        """

    def get_active_timezone(self):
        """
        gets the application active timezone.

        :rtype: tzinfo
        """

        return self.__active_timezone
