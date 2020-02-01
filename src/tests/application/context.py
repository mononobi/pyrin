# -*- coding: utf-8 -*-
"""
application context module.
"""

import pyrin.utils.unique_id as uuid_utils
import pyrin.globalization.datetime.services as datetime_services

from pyrin.core.context import CoreObject, Context
from pyrin.settings.static import APPLICATION_ENCODING, DEFAULT_COMPONENT_KEY


class CoreRequestMock(CoreObject):
    """
    core request mock class.
    """

    # charset of the request.
    charset = APPLICATION_ENCODING

    def __init__(self):
        super().__init__()

        self.request_id = uuid_utils.generate_uuid4()
        self.request_date = datetime_services.now()
        self.user = None
        self.component_custom_key = DEFAULT_COMPONENT_KEY
        self.context = Context()
        self.headers = Context()

    def __str__(self):
        result = 'request id: "{request_id}", request date: "{request_date}", ' \
                 'user: "{user}", component_custom_key: "{component}"'
        return result.format(request_id=self.request_id,
                             request_date=self.request_date,
                             user=self.user,
                             component=self.component_custom_key)

    def __hash__(self):
        return hash(self.request_id)
