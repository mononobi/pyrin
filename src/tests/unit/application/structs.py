# -*- coding: utf-8 -*-
"""
application structs module.
"""

from pyrin.application.base import Application
from pyrin.application.structs import Component
from pyrin.core.structs import Manager
from pyrin.processor.request.wrappers.base import CoreRequest


class ApplicationMock(Application):
    """
    application mock class.
    """
    pass


class CoreRequestMock(CoreRequest):
    """
    core request mock class.
    """

    def __init__(self):
        super().__init__({}, populate_request=True)


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
