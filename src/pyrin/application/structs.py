# -*- coding: utf-8 -*-
"""
application structs module.
"""

from threading import Lock

from pyrin.core.structs import Context, CoreObject, UniqueSingletonMeta
from pyrin.settings.static import DEFAULT_COMPONENT_KEY
from pyrin.application.exceptions import ComponentAttributeError, InvalidComponentNameError


class ApplicationContext(Context):
    """
    context class to hold application contextual data.
    """

    attribute_error_message = 'Property [{name}] not found in application context.'


class ApplicationComponent(ApplicationContext):
    """
    context class to hold application components.
    """

    attribute_error = ComponentAttributeError
    attribute_error_message = 'Component [{name}] is not available in application components.'


class Component(CoreObject):
    """
    base component class.

    all component classes must inherit from this class and their respective manager class.
    """

    def __init__(self, component_name, **options):
        """
        initializes an instance of Component.

        :param str component_name: component name.

        :keyword object component_custom_key: component custom key.
        """

        super().__init__()

        # component id is a tuple[str, object] and should be unique for each
        # instance unless it's intended to replace an already existing one.
        self._component_id = self.make_component_id(component_name, **options)

    def get_id(self):
        """
        gets the component id of this instance.

        :rtype: tuple[str, object]
        """

        return self._component_id

    @staticmethod
    def make_component_id(component_name, **options):
        """
        makes a component id based on input values and returns it.

        :param str component_name: component name.

        :keyword object component_custom_key: component custom key.

        :raises InvalidComponentNameError: invalid component name.

        :rtype: tuple[str, object]
        """

        if component_name is None or len(component_name.strip()) <= 0:
            raise InvalidComponentNameError('Component name should not be None.')

        component_custom_key = options.get('component_custom_key', DEFAULT_COMPONENT_KEY)
        return component_name, component_custom_key


class ApplicationSingletonMeta(UniqueSingletonMeta):
    """
    application singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    instance = None
    _lock = Lock()
