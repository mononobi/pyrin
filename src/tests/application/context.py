# -*- coding: utf-8 -*-
"""
application context module.
"""

import pyrin.utils.unique_id as uuid_utils
import pyrin.globalization.datetime.services as datetime_services

from pyrin.application.context import Component
from pyrin.core.context import CoreObject, Context, Manager
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


class OnlyManagerMock(Manager):
    """
    only manager mock class.
    """
    pass


class OnlyComponentMock(Component):
    """
    only component mock class.
    """
    pass


class ComponentMock(Component, Manager):
    """
    component mock class.
    """
    pass


class DatabaseComponentMock(Component, Manager):
    """
    database component mock class.
    """
    pass


class ExtraDatabaseComponentMock(Component, Manager):
    """
    extra database component mock class.
    """
    pass


class DuplicateExtraDatabaseComponentMock(Component, Manager):
    """
    duplicate extra database component mock class.
    """
    pass


class DuplicateDatabaseComponentMock(Component, Manager):
    """
    duplicate database component mock class.
    """
    pass


class ComponentWithInvalidNameMock(Component, Manager):
    """
    component with invalid name mock class.
    """
    pass


class DuplicateComponentMock(Component, Manager):
    """
    duplicate component mock class.
    """
    pass


class DuplicateComponentForReplaceMock(Component, Manager):
    """
    duplicate component for replace mock class.
    """
    pass


class ExtraDuplicateComponentForReplaceMock(Component, Manager):
    """
    extra duplicate component for replace mock class.
    """
    pass


class ComponentWithCustomAttributesMock(Component, Manager):
    """
    component with custom attributes mock class.
    """
    pass


class DuplicateComponentWithCustomAttributesMock(Component, Manager):
    """
    duplicate component with custom attributes mock class.
    """
    pass


class ComponentWithInvalidCustomKeyMock(Component, Manager):
    """
    component with invalid custom key mock class.
    """
    pass


class DuplicateComponentWithInvalidCustomKeyMock(Component, Manager):
    """
    duplicate component with invalid custom key mock class.
    """
    pass
