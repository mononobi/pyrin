# -*- coding: utf-8 -*-
"""
admin page base module.
"""

import inspect

from sqlalchemy.sql.elements import Label, and_, or_
from sqlalchemy.orm import InstrumentedAttribute

import pyrin.utils.path as path_utils
import pyrin.utils.string as string_utils
import pyrin.utils.sqlalchemy as sqla_utils
import pyrin.utils.misc as misc_utils
import pyrin.utils.dictionary as dict_utils
import pyrin.admin.services as admin_services
import pyrin.filtering.services as filtering_services
import pyrin.validator.services as validator_services
import pyrin.security.session.services as session_services
import pyrin.database.model.services as model_services
import pyrin.configuration.services as config_services
import pyrin.database.paging.services as paging_services
import pyrin.utilities.string.normalizer.services as string_normalizer_services

from pyrin.core.globals import _
from pyrin.core.structs import SecureList
from pyrin.admin.interface import AbstractAdminPage
from pyrin.admin.page.schema import AdminSchema
from pyrin.core.globals import SECURE_TRUE
from pyrin.admin.page.mixin import AdminPageCacheMixin
from pyrin.caching.mixin.decorators import fast_cache
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.paging.paginator import SimplePaginator
from pyrin.database.services import get_current_store
from pyrin.database.model.base import BaseEntity
from pyrin.logging.contexts import suppress
from pyrin.security.session.enumerations import RequestContextEnum
from pyrin.validator.exceptions import ValidationError
from pyrin.admin.page.enumerations import TableTypeEnum, PaginationTypeEnum, \
    PaginationPositionEnum, FormatEnum, MonthFormatEnum, ButtonTypeEnum, \
    LinkTypeEnum, HourCycleEnum
from pyrin.admin.page.exceptions import InvalidListFieldError, ListFieldRequiredError, \
    InvalidMethodNameError, InvalidAdminEntityTypeError, AdminNameRequiredError, \
    AdminRegisterNameRequiredError, RequiredValuesNotProvidedError, \
    CompositePrimaryKeysNotSupportedError, DuplicateListFieldNamesError, \
    InvalidListSearchFieldError, DuplicateListSearchFieldNamesError, EntityNotFoundError, \
    InvalidListFieldNameError, ExtraDataFieldsAndEntityFieldsOverlapError


class AdminPage(AbstractAdminPage, AdminPageCacheMixin):
    """
    admin page class.

    all admin pages must be subclassed from this.
    """

    # ===================== REQUIRED CONFIGS ===================== #

    # the entity class that this admin page represents.
    entity = None

    # name of this admin page to be used for registration.
    # the register name is case-insensitive and must be unique for each admin page.
    # this name will also be used for generating admin page api routes.
    register_name = None

    # singular name of this admin page for representation.
    name = None

    # ===================== LIST CONFIGS ===================== #

    # columns to show in list view. it could be a column attribute, an expression
    # level hybrid property or a string method name of this admin page.
    # the method should accept a single positional argument as current row.
    # for example: (UserEntity.id, UserEntity.fullname, 'title', UserDetailEntity.age)
    list_fields = ()

    # columns that will be selected from database and will be used to compute
    # another field's value but they will be removed from the final result and
    # will not be returned to client.
    # it could be a column attribute or an expression level hybrid property.
    # for example: (UserEntity.id, UserEntity.fullname, UserDetailEntity.age)
    list_temp_fields = ()

    # specifies that if 'list_fields' is not provided only show readable
    # columns of the entity in list view.
    list_only_readable = True

    # specifies that if 'list_fields' are not provided also show pk columns in list view.
    # note that if the admin page has get permission, pk columns will always be added.
    list_pk = True

    # specifies that if 'list_fields' are not provided also show fk columns in list view.
    list_fk = True

    # specifies that if 'list_fields' are not provided also show expression
    # level hybrid property columns in list view.
    list_expression_level_hybrid_properties = True

    # list of default ordering columns.
    # it must be string names from 'list_fields' or 'list_temp_fields'.
    # for example: ('first_name', '-last_name')
    list_ordering = ()

    # specifies that each row must have an index in it.
    list_indexed = False

    # list index name to be added to each row.
    list_index_name = None

    # start index of rows.
    list_start_index = 1

    # columns to show in list filter.
    list_filters = ()

    # paginate results in list view.
    list_paged = True

    # records per page.
    # it could not be more than 'list_max_page_size', otherwise it
    # will be corrected silently.
    list_page_size = None

    # max records per page.
    # it could not be more than 'max_page_size' from 'database'
    # config store, otherwise it will be corrected silently.
    list_max_page_size = None

    # pagination type to be used on client if paging is enabled for this admin page.
    # it should be from 'PaginationTypeEnum' values.
    list_pagination_type = PaginationTypeEnum.NORMAL

    # pagination position to be used on client if paging is enabled for this admin page.
    # it should be from 'PaginationPositionEnum' values.
    list_pagination_position = PaginationPositionEnum.BOTTOM

    # a value to be shown when the relevant data is null.
    list_null_value = '-'

    # a dict containing field names and their list field type for fields which their
    # type could not be detected automatically. for example hybrid property fields
    # or fields which their value is coming from a method of this admin page.
    # note that the provided types must be from 'ListFieldTypeEnum' values.
    # for example: {'is_viewed': ListFieldTypeEnum.BOOLEAN}
    list_extra_field_types = {}

    # a value to define client-side table type.
    # it should be from 'TableTypeEnum' values.
    list_table_type = TableTypeEnum.DENSE

    # enable exporting the currently active page into pdf or csv file.
    list_enable_export = True

    # a file name to be used for exporting data. for example: Users
    # if not provided defaults to this admin page's plural name.
    list_export_name = None

    # create a link to related admin detail page for all pk columns.
    # this only has effect if the related admin page has get permission.
    list_link_pk = True

    # create a link to related admin detail page for all fk columns.
    # this only has effect if the related admin page has get permission.
    list_link_fk = True

    # let user select which columns to show on list page.
    list_column_selection = True

    # let user re-order table columns on list page.
    list_column_ordering = True

    # let user group results by columns on list page.
    list_grouping = False

    # specifies that client should render a search box to let user filter the
    # results by any of columns which are involved in this admin page list view.
    list_search = True

    # a number in milliseconds to be used as debounce interval in client search box.
    # note that if you set it to lower numbers, it will result in a service call
    # for each keystroke in search box.
    list_search_debounce_interval = 700

    # extra columns to let user filter by their value in list view.
    # it must be a column attribute or a labeled column.
    # this is useful if you want to add some extra fields for searching but do not
    # want to add these columns in 'list_fields'.
    # the main usage for this attribute is to set labeled columns for columns
    # of different entities which have the same name.
    # for example:
    # (UserEntity.last_name, UserEntity.name, CityEntity.name.label('city_name'))
    list_search_fields = ()

    # format to render datetime fields on list page.
    list_datetime_format = dict(year=FormatEnum.NUMERIC,
                                month=MonthFormatEnum.SHORT,
                                day=FormatEnum.NUMERIC,
                                hour=FormatEnum.TWO_DIGIT,
                                minute=FormatEnum.TWO_DIGIT,
                                second=FormatEnum.TWO_DIGIT,
                                hourCycle=HourCycleEnum.H23)

    # format to render date fields on list page.
    list_date_format = dict(year=FormatEnum.NUMERIC,
                            month=MonthFormatEnum.SHORT,
                            day=FormatEnum.NUMERIC)

    # format to render time fields on list page.
    list_time_format = dict(hour=FormatEnum.TWO_DIGIT,
                            minute=FormatEnum.TWO_DIGIT,
                            second=FormatEnum.TWO_DIGIT,
                            hourCycle=HourCycleEnum.H23)

    # a locale to be used to render date and time fields on list page.
    # for example: 'en-US', 'fa' or ...
    # if not provided, the locale on client browser will be used.
    list_locale = None

    # a value to be used as max body height for table in list view.
    # for example: '800px'
    # if not set, the client will automatically choose the best height
    # based on the screen resolution.
    list_max_body_height = None

    # ===================== SERVICE CONFIGS ===================== #

    # a service to be used for create operation.
    # if not set, the default create operation of this admin page will be used.
    # the create service must also accept keyword arguments.
    create_service = None

    # a service to be used for update operation.
    # if not set, the default update operation of this admin page will be used.
    # the update service must accept a positional argument at the beginning as
    # the primary key of the related entity and also accept keyword arguments.
    update_service = None

    # a service to be used for remove operation.
    # if not set, the default remove operation of this admin page will be used.
    # the remove service must accept a single positional argument as the
    # primary key of the related entity.
    remove_service = None

    # ===================== PERMISSION CONFIGS ===================== #

    # specifies that this admin page has get permission.
    # note that if entity has composite primary key, it does not
    # have get permission and this value will be ignored.
    get_permission = True

    # specifies that this admin page has create permission.
    create_permission = True

    # specifies that this admin page has update permission.
    # note that if entity has composite primary key, it does not
    # have update permission and this value will be ignored.
    update_permission = True

    # specifies that this admin page has single or bulk remove permission.
    # note that if entity has composite primary key, it does not have single
    # or bulk remove permission and this value will be ignored.
    remove_permission = True

    # specifies that this admin page has remove all permission.
    remove_all_permission = True

    # ===================== OTHER CONFIGS ===================== #

    # the category name to register this admin page in it.
    # all admin pages with the same category will be grouped together.
    # the category name is case-insensitive.
    # it will be set to the package name of current admin page if not provided.
    category = None

    # plural name of this admin page for representation.
    # it will be automatically generated from 'name' if not provided.
    plural_name = None

    # extra field names that are required to be provided for create and are
    # optional for update but they are not a field of the entity itself.
    # in the form of:
    # {str field_name: type python_type}
    # for example:
    # {'password': str, 'join_date': datetime, 'age': int}
    # if the provided names have related validators, the
    # info of that validator will be sent to client.
    extra_data_fields = {}

    # ===================== INTERNAL CONFIGS ===================== #

    # paginator class to be used.
    paginator_class = SimplePaginator

    # the fully qualified name of find api.
    FIND_ENDPOINT = 'pyrin.admin.api.find'

    def __init__(self, *args, **options):
        """
        initializes an instance of AdminPage.

        :raises InvalidAdminEntityTypeError: invalid admin entity type error.
        :raises AdminRegisterNameRequiredError: admin register name required error.
        :raises AdminNameRequiredError: admin name required error.
        """

        super().__init__()

        if not inspect.isclass(self.entity) or not issubclass(self.entity, BaseEntity):
            raise InvalidAdminEntityTypeError('The entity for [{admin}] class '
                                              'must be a subclass of [{base}].'
                                              .format(admin=self, base=BaseEntity))

        if self.register_name in (None, '') or self.register_name.isspace():
            raise AdminRegisterNameRequiredError('The register name for '
                                                 '[{admin}] class is required.'
                                                 .format(admin=self))

        if self.name in (None, '') or self.name.isspace():
            raise AdminNameRequiredError('The name for [{admin}] class is required.'
                                         .format(admin=self))

        # list of method names of this admin page to be used for processing the list results.
        self._method_names = self._extract_method_names()
        self._schema = AdminSchema(self,
                                   indexed=self.list_indexed,
                                   start_index=self.list_start_index,
                                   index_name=self.list_index_name,
                                   exclude=self._get_list_temp_field_names())
        self._paginator = None
        if self.list_paged is True:
            self._paginator = self.paginator_class(self.FIND_ENDPOINT,
                                                   page_size=self._get_page_size(),
                                                   max_page_size=self._get_max_page_size())

    def _get_hidden_pk_name(self):
        """
        gets hidden pk name from configs.

        :rtype: str
        """

        return config_services.get_active('admin', 'hidden_pk_name')

    def _get_search_param(self):
        """
        gets search param name from configs.

        :rtype: str
        """

        return config_services.get_active('admin', 'search_param')

    @fast_cache
    def _get_list_export_name(self):
        """
        gets a file name to be used for exporting data on list page.

        :rtype: str
        """

        if self.list_export_name:
            return self.list_export_name

        return self.get_plural_name()

    def _get_column_title(self, name):
        """
        gets the column title of given field name for list page.

        :param str name: field name.

        :raises InvalidListFieldNameError: invalid list field name error.

        :rtype: str
        """

        if name is None:
            raise InvalidListFieldNameError('There are some fields in "list_fields" of '
                                            '[{admin}] class which does not have a name. '
                                            'use label to set a name for them.'
                                            .format(admin=self))

        name = name.replace('_', ' ')
        return name.upper()

    def _get_field_title(self, name):
        """
        gets the field title of given field name for detail and create page.

        :param str name: field name.

        :rtype: str
        """

        name = name.replace('_', ' ')
        return string_normalizer_services.title_case(name)

    @classmethod
    @fast_cache
    def _get_primary_key_name(cls):
        """
        gets the name of the primary key of this admin page's related entity.

        note that if the entity has a composite primary key, this method raises an error.

        :rtype: str
        """

        if len(cls.entity.primary_key_columns) == 1:
            return cls.entity.primary_key_columns[0]

        raise CompositePrimaryKeysNotSupportedError('Composite primary keys are not '
                                                    'supported for admin page.')

    @classmethod
    def _get_primary_key_holder(cls, pk):
        """
        gets a dict with the primary key name of this page's entity set to the given value.

        :param object pk: value to be set to primary key.

        :rtype: dict
        """

        pk_name = cls._get_primary_key_name()
        pk_holder = dict()
        pk_holder[pk_name] = pk

        return pk_holder

    def _is_valid_field(self, field):
        """
        gets a value indicating that the provided field is a valid field for list fields.

        :param object field: field to be checked.

        :rtype: bool
        """

        return hasattr(field, 'key')

    def _is_valid_method(self, name):
        """
        gets a value indicating that the provided name is a valid method name of this admin page.

        :param str name: method name.

        :rtype: bool
        """

        method = getattr(self, name, None)
        return callable(method)

    def _is_list_pk_required(self):
        """
        gets a value indicating that primary key column for list view is required.

        it returns True if this admin page has any of `get` or `remove` permissions.

        :rtype: bool
        """

        return self.has_get_permission() or self.has_remove_permission()

    @fast_cache
    def _extract_method_names(self):
        """
        extracts all valid method names from list fields.

        :rtype: tuple[str]
        """

        names = []
        if self.list_fields:
            for item in self.list_fields:
                if isinstance(item, str) and self._is_valid_method(item):
                    names.append(item)

        return tuple(names)

    def _extract_field_names(self, fields, allow_string=True):
        """
        extracts fields names form given fields

        :param list | tuple fields: list of fields to extract their names.

        :param bool allow_string: specifies that string fields should also
                                  be accepted. defaults to True if not provided.

        :raises InvalidListFieldError: invalid list field error.

        :rtype: tuple[str]
        """

        names = []
        for item in fields:
            if self._is_valid_field(item):
                names.append(item.key)
            elif allow_string is True and isinstance(item, str) \
                    and self._is_valid_method(item):
                names.append(item)
            else:
                message = 'Provided field [{field}] is not a valid value. ' \
                          'it must be a column attribute{sign} ' \
                          'expression level hybrid property{end}'

                if allow_string is True:
                    message = message.format(
                        field=str(item), sign=',',
                        end=' or a string representing a method name of [{admin}] class.')
                else:
                    message = message.format(field=str(item), sign=' or',
                                             end='.')

                raise InvalidListFieldError(message.format(admin=self))

        return tuple(names)

    @fast_cache
    def _get_list_field_names(self):
        """
        gets all list field names of this admin page.

        :raises InvalidListFieldError: invalid list field error.
        :raises DuplicateListFieldNamesError: duplicate list field names error.

        :rtype: tuple[str]
        """

        all_fields = ()
        if not self.list_fields:
            all_fields = self._get_default_list_fields()
        else:
            all_fields = list(self.list_fields)
            if self._is_list_pk_required():
                self._inject_primary_key(all_fields)

        all_fields = self._extract_field_names(all_fields, allow_string=True)
        if self.list_indexed is True:
            index_name = self.list_index_name
            if index_name in (None, ''):
                index_name = config_services.get('api', 'schema', 'index_name')

            all_fields = list(all_fields)
            all_fields.insert(0, index_name)
            all_fields = tuple(all_fields)

        duplicates = misc_utils.get_duplicates(all_fields)
        if duplicates:
            raise DuplicateListFieldNamesError('There are some duplicate field names '
                                               'in "list_fields" of [{admin}] class. '
                                               'this will make the find result incorrect. '
                                               'please remove duplicate fields or set '
                                               'unique labels for them: {duplicates}'
                                               .format(admin=self, duplicates=duplicates))

        return all_fields

    def _get_attribute(self, item):
        """
        gets the related instrumented or hybrid property attribute to given item.

        it may return the same value if it is already an instrumented or
        hybrid property attribute. it may return None if no related instrumented
        or hybrid property attribute could be found.

        :param InstrumentedAttribute | Label | hybrid_property item: item to get its
                                                                     related attribute.

        :rtype: sqlalchemy.orm.InstrumentedAttribute | sqlalchemy.ext.hybrid.hybrid_property
        """

        if isinstance(item, InstrumentedAttribute) or \
                sqla_utils.is_expression_level_hybrid_property(item):
            return item
        elif isinstance(item, Label):
            hybrid_property = getattr(item, '_hybrid_property', None)
            if hybrid_property is not None:
                return hybrid_property
            elif item.base_columns:
                columns = list(item.base_columns)
                if isinstance(columns[0], CoreColumn):
                    return model_services.get_instrumented_attribute(columns[0])

        return None

    def _get_list_field_column(self, name):
        """
        gets the relevant column or hybrid property attribute for given field name.

        it may return None if no related column or hybrid property could be found.

        :param str name: field name.

        :rtype: sqlalchemy.orm.InstrumentedAttribute | sqlalchemy.ext.hybrid.hybrid_property
        """

        selectable_fields = self._get_list_fields()
        for item in selectable_fields:
            if self._is_valid_field(item) and item.key == name:
                return self._get_attribute(item)

        return None

    @fast_cache
    def _get_link_methods(self):
        """
        gets all method names which should render a link on client list view.

        :rtype: tuple[str]
        """

        links = []
        for name in self.method_names:
            method = getattr(self, name)
            is_link = getattr(method, 'is_link', False)
            if is_link is True:
                links.append(name)

        return tuple(links)

    @fast_cache
    def _get_list_fields_to_column_map(self):
        """
        gets a dict of all list field names and their related columns.

        the column value may be None if the name does not belong to a
        column or hybrid property. for example method names.

        :returns: dict(InstrumentAttribute | hybrid_property name)
        :rtype: dict
        """

        result = dict()
        all_fields = self._get_list_field_names()
        for name in all_fields:
            attribute = self._get_list_field_column(name)
            result[name] = attribute

        return result

    @fast_cache
    def _get_list_search_fields_to_column_map(self):
        """
        gets a dict of all list search field names and their related columns.

        :raises InvalidListSearchFieldError: invalid list search field error.
        :raises DuplicateListSearchFieldNamesError: duplicate list search field names error.

        :returns: dict(InstrumentAttribute | hybrid_property name)
        :rtype: dict
        """

        if self.list_search_fields:
            names = []
            for item in self.list_search_fields:
                if not isinstance(item, (InstrumentedAttribute, Label)) and \
                        not sqla_utils.is_expression_level_hybrid_property(item):
                    raise InvalidListSearchFieldError('Provided field [{field}] is not a valid '
                                                      'list search field for [{admin}] class. '
                                                      'search fields must be a column attribute '
                                                      'or an expression level hybrid property.'
                                                      .format(admin=self, field=str(item)))

                names.append(item.key)

            duplicates = misc_utils.get_duplicates(names)
            if duplicates:
                raise DuplicateListSearchFieldNamesError('There are some duplicate field names '
                                                         'in "list_search_fields" of [{admin}] '
                                                         'class. please remove duplicate fields '
                                                         'or set unique labels for them: '
                                                         '{duplicates}'
                                                         .format(admin=self,
                                                                 duplicates=duplicates))

        result = dict()
        list_fields = self._get_list_fields_to_column_map()
        for name, column in list_fields.items():
            if column is not None and name != self._get_hidden_pk_name():
                result[name] = column

        if self.list_search_fields:
            for item in self.list_search_fields:
                attribute = self._get_attribute(item)
                if attribute is not None:
                    result[item.key] = attribute
                elif sqla_utils.is_expression_level_hybrid_property(item):
                    result[item.key] = item

        return result

    def _get_pk_info(self, column):
        """
        gets a dict containing pk info for given column if required.

        :param InstrumentedAttribute column: column to be checked.

        :returns: dict(bool is_pk,
                       str pk_register_name,
                       str pk_name)
        :rtype: dict
        """

        result = dict(is_pk=False, pk_register_name=None)
        if sqla_utils.is_expression_level_hybrid_property(column) or \
                not column.property or not column.property.columns:
            return result

        base_column = column.property.columns[0]
        is_pk = base_column.primary_key
        if is_pk is True:
            admin_page = admin_services.try_get_admin_page(column.class_)
            if admin_page is not None and admin_page.has_get_permission() is True:
                result.update(is_pk=is_pk,
                              pk_register_name=admin_page.get_register_name(),
                              pk_name=admin_page.get_singular_name())

        return result

    def _get_fk_info(self, column):
        """
        gets a dict containing fk info for given column if required.

        :param InstrumentedAttribute column: column to be checked.

        :returns: dict(bool is_fk,
                       str fk_register_name,
                       str fk_name)
        :rtype: dict
        """

        result = dict(is_fk=False, fk_register_name=None)
        if sqla_utils.is_expression_level_hybrid_property(column) or \
                not column.property or not column.property.columns:
            return result

        base_column = column.property.columns[0]
        is_fk = base_column.is_foreign_key
        if is_fk is True:
            foreign_keys = list(base_column.foreign_keys)
            if foreign_keys and foreign_keys[0].constraint:
                entity = sqla_utils.get_class_by_table(model_services.get_declarative_base(),
                                                       foreign_keys[0].constraint.referred_table,
                                                       raise_multi=False)

                if entity is not None:
                    admin_page = admin_services.try_get_admin_page(entity)
                    if admin_page is not None and admin_page.has_get_permission() is True:
                        result.update(is_fk=is_fk,
                                      fk_register_name=admin_page.get_register_name(),
                                      fk_name=admin_page.get_singular_name())

        return result

    def _get_extra_list_field_info(self, name):
        """
        gets a dict of extra info for given list field.

        it may return an empty dict.

        :param str name: list field name.

        :rtype: dict
        """

        result = dict()
        column_map = self._get_list_fields_to_column_map()
        attribute = column_map.get(name)
        type_ = None
        if attribute is not None:
            validator = validator_services.try_get_validator(attribute.class_, attribute)
            if validator is not None:
                info = validator.get_info()
                type_ = admin_services.get_list_field_type(info.get('form_field_type'))
                lookup = info.get('in_enum_lookup')
                if lookup:
                    result.update(lookup=lookup)

            result.update(self._get_pk_info(attribute))
            result.update(self._get_fk_info(attribute))

        elif self.list_extra_field_types:
            type_ = self.list_extra_field_types.get(name)

        if type_ is not None:
            result.update(type=type_)

        return result

    @fast_cache
    def _get_list_datasource_info(self):
        """
        gets datasource info to be used for list page.

        :rtype: tuple[dict]
        """

        results = []
        all_fields = self._get_list_field_names()
        sortable_fields = self._get_sortable_fields()
        link_methods = self._get_link_methods()
        hidden_pk_name = self._get_hidden_pk_name()
        for item in all_fields:
            info = dict(field=item,
                        title=self._get_column_title(item),
                        sorting=item in sortable_fields,
                        emptyValue=self.list_null_value,
                        is_link=item in link_methods)

            if item in link_methods or item == hidden_pk_name:
                info.update(export=False)

            if item == hidden_pk_name:
                info.update(hidden=True, hiddenByColumnsButton=True)
            else:
                extra_info = self._get_extra_list_field_info(item)
                info.update(extra_info)

            results.append(info)

        return tuple(results)

    @fast_cache
    def _get_primary_keys(self):
        """
        gets all primary key attributes of this admin page's related entity.

        :rtype: tuple[InstrumentedAttribute]
        """

        return tuple(self.entity.get_attribute(name)
                     for name in self.entity.primary_key_columns)

    def _inject_primary_key(self, fields):
        """
        injects primary key attribute of related entity into given list.

        this is required if the current admin page has any
        of get, remove or update permissions. note that only single
        primary keys are allowed. otherwise it raises an error.

        :param list fields: fields to inject primary key into it.

        :raises CompositePrimaryKeysNotSupportedError: composite primary keys not supported error.
        """

        if not self._has_single_primary_key():
            raise CompositePrimaryKeysNotSupportedError('Composite primary keys are not '
                                                        'supported for admin page.')

        primary_key = self._get_primary_keys()[0]
        fields.append(primary_key.label(self._get_hidden_pk_name()))

    @fast_cache
    def _get_list_temp_field_names(self):
        """
        gets all list temp field names of this admin page.

        :raises InvalidListFieldError: invalid list field error.

        :rtype: tuple[str]
        """

        if not self.list_temp_fields:
            return tuple()

        return self._extract_field_names(self.list_temp_fields, allow_string=False)

    @fast_cache
    def _get_default_list_fields(self):
        """
        gets defaults list fields for this admin page.

        :rtype: tuple
        """

        primary_keys = []
        primary_key_names = ()
        foreign_keys = []
        foreign_key_names = ()
        columns = []
        column_names = ()
        expression_level_hybrid_properties = []
        expression_level_hybrid_property_names = ()

        if self.list_only_readable is True:
            column_names = self.entity.readable_columns
            if self.list_pk is True:
                primary_key_names = self.entity.readable_primary_key_columns

            if self.list_fk is True:
                foreign_key_names = self.entity.readable_foreign_key_columns
        else:
            column_names = self.entity.all_columns
            if self.list_pk is True:
                primary_key_names = self.entity.primary_key_columns

            if self.list_fk is True:
                foreign_key_names = self.entity.foreign_key_columns

        if self.list_expression_level_hybrid_properties is True:
            expression_level_hybrid_property_names = \
                self.entity.expression_level_hybrid_properties

        for pk in primary_key_names:
            primary_keys.append(self.entity.get_attribute(pk))

        for fk in foreign_key_names:
            foreign_keys.append(self.entity.get_attribute(fk))

        for column in column_names:
            columns.append(self.entity.get_attribute(column))

        for hybrid_property in expression_level_hybrid_property_names:
            attribute = self.entity.get_attribute(hybrid_property)
            expression_level_hybrid_properties.append(attribute.label(attribute.key))

        primary_keys.extend(foreign_keys)
        primary_keys.extend(columns)
        primary_keys.extend(expression_level_hybrid_properties)

        if self._is_list_pk_required():
            self._inject_primary_key(primary_keys)

        return tuple(primary_keys)

    @fast_cache
    def _get_list_fields(self):
        """
        gets all fields from `list_fields` that are column or hybrid property.

        :rtype: tuple
        """

        if not self.list_fields:
            return self._get_default_list_fields()

        results = []
        for item in self.list_fields:
            if self._is_valid_field(item):
                if sqla_utils.is_expression_level_hybrid_property(item):
                    labeled_item = item.label(item.key)
                    setattr(labeled_item, '_hybrid_property', item)
                    results.append(labeled_item)
                else:
                    results.append(item)

        if self._is_list_pk_required():
            self._inject_primary_key(results)

        return tuple(results)

    @fast_cache
    def _get_list_temp_fields(self):
        """
        gets all fields from `list_temp_fields`.

        :rtype: tuple
        """

        if not self.list_temp_fields:
            return tuple()

        results = [item for item in self.list_temp_fields if self._is_valid_field(item)]
        return tuple(results)

    @fast_cache
    def _get_selectable_fields(self):
        """
        gets all selectable fields of this admin page.

        :raises ListFieldRequiredError: list field required error.

        :rtype: tuple
        """

        results = self._get_list_fields() + self._get_list_temp_fields()
        if len(results) <= 0:
            raise ListFieldRequiredError('At least a single column attribute or '
                                         'expression level hybrid property must be '
                                         'provided in list fields or list temp fields '
                                         'of [{admin}] class.'.format(admin=self))

        return results

    def _perform_joins(self, query, **options):
        """
        performs joins on given query and returns a new query object.

        this method is intended to be overridden in subclasses if you want to
        provide columns of other entities in `list_fields` or `list_temp_fields`.

        :param CoreQuery query: query instance.

        :rtype: CoreQuery
        """

        return query

    def _prepare_inclusive_filters(self, search_text, filters, labeled_filters):
        """
        prepares inclusive filters.

        :param str search_text: search text.
        :param dict filters: filters which have been provided by client.
        :param dict labeled_filters: dict of filter names to column map.
        """

        for name, column in labeled_filters.items():
            value = None
            if sqla_utils.is_expression_level_hybrid_property(column):
                value = search_text
            else:
                with suppress(ValidationError, log=False):
                    value = validator_services.validate_field(column.class_, column,
                                                              search_text, for_find=True)

            if value is not None:
                filters[name] = value

    def _filter_query(self, query, **filters):
        """
        filters given query and returns a new query object.

        :param CoreQuery query: query instance.

        :rtype: CoreQuery
        """

        labeled_filters = self._get_list_search_fields_to_column_map()
        search_text = filters.pop(self._get_search_param(), None)
        type_ = and_
        if self.list_search is True and search_text not in (None, ''):
            type_ = or_
            self._prepare_inclusive_filters(search_text, filters, labeled_filters)

        expressions = filtering_services.filter(filters, labeled_filters=labeled_filters)
        return query.filter(type_(*expressions))

    def _validate_filters(self, filters):
        """
        validates given filters.

        :param dict filters: filters to be validated.

        :raises ValidationError: validation error.
        """

        validator_services.validate_for_find(self.entity, filters)

    def _perform_order_by(self, query, **filters):
        """
        performs order by on given query and returns a new query object.

        :param CoreQuery query: query instance.

        :keyword str | list[str] order_by: order by columns.
                                           if not provided, defaults to `ordering`
                                           fields of this admin class.
        :rtype: CoreQuery
        """

        filters.update(labeled_columns=SecureList(self._get_list_labels()))
        force_order = list(self.list_ordering or [])
        force_order.extend(self.entity.primary_key_columns)
        return query.safe_order_by(self._get_list_entities(), *force_order, **filters)

    @fast_cache
    def _get_page_size(self):
        """
        gets page size of this admin page.

        :rtype: int
        """

        max_page_size = self._get_max_page_size()
        default_page_size = config_services.get('database', 'paging', 'default_page_size')
        page_size = self.list_page_size
        if page_size is None or page_size < 1 or page_size > max_page_size:
            page_size = min(default_page_size, max_page_size)

        return page_size

    @fast_cache
    def _get_max_page_size(self):
        """
        gets max page size of this admin page.

        :rtype: int
        """

        global_max_page_size = config_services.get('database', 'paging', 'max_page_size')
        max_page_size = self.list_max_page_size
        if max_page_size is None or max_page_size < 1 or max_page_size > global_max_page_size:
            max_page_size = global_max_page_size

        return max_page_size

    def _get_paginator(self):
        """
        gets paginator for this admin page.

        :rtype: PaginatorBase
        """

        return self._paginator.copy()

    def _inject_paginator(self, filters):
        """
        injects this admin page's paginator into current request context.

        :param dict filters: view function inputs.
        """

        paginator = self._get_paginator()
        paging_services.inject_paginator(paginator, filters)

    def _paginate_query(self, query, **filters):
        """
        paginates given query and returns a new query object.

        it may return the same query if pagination is disabled for this admin page.

        :param CoreQuery query: query instance.

        :keyword CoreColumn column: column to be used in count function.
                                    defaults to `*` if not provided.
                                    this is only used if `inject_total` is
                                    provided and a single query could be
                                    produced for count.

        :keyword bool distinct: specifies that count should
                                be executed on distinct select.
                                defaults to False if not provided.
                                note that `distinct` will only be
                                used if `column` is also provided.

        :keyword int __limit__: limit value.
        :keyword int __offset__: offset value.

        :rtype: CoreQuery
        """

        if self.list_paged is True:
            self._inject_paginator(filters)
            return query.paginate(inject_total=SECURE_TRUE, **filters)

        return query

    @fast_cache
    def _get_page_size_options(self):
        """
        gets a tuple of page size options of this admin page.

        :rtype: tuple[int] | tuple[int, int]
        """

        page_size = self._get_page_size()
        max_page_size = self._get_max_page_size()
        if page_size == max_page_size:
            return page_size,

        return page_size, max_page_size

    def _process_find_results(self, results, **options):
        """
        processes the given results and returns a list of serialized values.

        :param list[ROW_RESULT] results: results to be processed.

        :rtype: list[dict]
        """

        paginator = session_services.get_request_context(RequestContextEnum.PAGINATOR)
        return self._schema.filter(results, paginator=paginator)

    @classmethod
    def _has_single_primary_key(cls):
        """
        gets a value indicating that the related entity has a single primary key.

        :rtype: bool
        """

        return len(cls.entity.primary_key_columns) == 1

    @classmethod
    def _validate_extra_fields(cls, data):
        """
        validates that all extra required fields are available in data.

        :param dict data: data to be validated.

        :raises RequiredValuesNotProvidedError: required values not provided error.
        """

        if not cls.extra_data_fields:
            return

        not_present = []
        for name in cls.extra_data_fields:
            if data.get(name) is None:
                not_present.append(name)

        not_present = set(not_present)
        if len(not_present) > 0:
            raise RequiredValuesNotProvidedError(_('These values are required: {values}')
                                                 .format(values=list(not_present)))

    @classmethod
    def _process_created_entity(cls, entity, **data):
        """
        processes created entity if required.

        it must change the attributes of given entity in-place.

        :param pyrin.database.model.base.BaseEntity entity: created entity.

        :keyword **data: all data that has been passed to create method.
        """
        pass

    @classmethod
    def _create(cls, **data):
        """
        creates an entity with given data.

        it's preferred for this method to return the pk of created entity
        if it is not a composite primary key. this lets the client to fill
        fk fields automatically after create.

        :keyword **data: all data to be passed to create method.

        :rtype: object
        """

        entity = cls.entity(**data)
        cls._process_created_entity(entity, **data)
        entity.save()
        if cls._has_single_primary_key():
            return entity.primary_key()

        return None

    @classmethod
    def _process_updated_entity(cls, entity, **data):
        """
        processes updated entity if required.

        it must change the attributes of given entity in-place.

        :param pyrin.database.model.base.BaseEntity entity: updated entity.

        :keyword **data: all data that has been passed to update method.
        """
        pass

    @classmethod
    def _get(cls, pk):
        """
        gets an entity with given primary key.

        :param object pk: primary key of entity to be get.

        :raises EntityNotFoundError: entity not found error.

        :rtype: pyrin.database.model.base.BaseEntity
        """

        store = get_current_store()
        entity = store.query(cls.entity).get(pk)
        if entity is None:
            raise EntityNotFoundError(_('{name} with primary key [{pk}] does not exist.')
                                      .format(name=cls.name, pk=pk))

        return entity

    @classmethod
    def _update(cls, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to update method.

        :raises EntityNotFoundError: entity not found error.
        """

        entity = cls._get(pk)
        entity.update(**data)
        cls._process_updated_entity(entity, **data)

    @classmethod
    def _remove(cls, pk):
        """
        deletes an entity with given pk.

        :param object pk: entity primary key to be deleted.
        """

        store = get_current_store()
        pk_name = cls._get_primary_key_name()
        pk_column = cls.entity.get_attribute(pk_name)
        store.query(cls.entity).filter(pk_column == pk).delete()

    def _remove_bulk(self, *pk):
        """
        deletes all entities with given primary keys.

        :param object pk: entity primary key to be deleted.
        """

        store = get_current_store()
        pk_name = self._get_primary_key_name()
        pk_column = self.entity.get_attribute(pk_name)
        store.query(self.entity).filter(pk_column.in_(pk)).delete()

    def _remove_all(self):
        """
        deletes all entities.
        """

        store = get_current_store()
        store.query(self.entity).delete()

    @fast_cache
    def _get_list_entities(self):
        """
        gets all entities that are involved in list select query.

        :rtype: tuple[type[BaseEntity]]
        """

        selectable_fields = self._get_selectable_fields()
        entities = []
        for item in selectable_fields:
            if isinstance(item, InstrumentedAttribute):
                entities.append(item.class_)

        return tuple(set(entities))

    @fast_cache
    def _get_list_labels(self):
        """
        gets all labels that are involved in list select query.

        :rtype: tuple[str]
        """

        selectable_fields = self._get_selectable_fields()
        labels = []
        for item in selectable_fields:
            if isinstance(item, Label) and item.key != self._get_hidden_pk_name():
                labels.append(item.key)

        return tuple(set(labels))

    @fast_cache
    def _get_sortable_fields(self):
        """
        gets all field names that could be used for result ordering by client.

        :rtype: tuple[str]
        """

        list_fields = self._get_list_fields()
        results = []
        for item in list_fields:
            if isinstance(item, (InstrumentedAttribute, Label)) \
                    and item.key != self._get_hidden_pk_name():
                results.append(item.key)

        return tuple(set(results))

    def _get_extra_data_fields(self, for_update):
        """
        gets all extra data fields of this admin page for specified operation.

        :param bool for_update: specifies that fields must be returned for which operation.

        :rtype: tuple[dict]
        """

        fields = []
        if self.extra_data_fields:
            for name, type_ in self.extra_data_fields.items():
                item = dict(field=name, is_fk=False, is_pk=False,
                            title=self._get_field_title(name),
                            form_field_type=validator_services.get_form_field_type(type_))
                validator = validator_services.try_get_validator(self.entity, name)
                if validator is not None:
                    item.update(validator.get_info(for_update))

                item.setdefault('required', not for_update)
                fields.append(item)

        return tuple(fields)

    def _get_data_field(self, name, for_update, primary_keys, foreign_keys):
        """
        gets info of given data field for specified operation.

        :param str name: field name.
        :param bool for_update: specifies that fields must be returned for which operation.
        :param tuple[str] primary_keys: all primary key names.
        :param tuple[str] foreign_keys: all foreign key names.

        :rtype: dict
        """

        is_fk = name in foreign_keys
        info = dict(field=name, title=self._get_field_title(name),
                    is_fk=is_fk, is_pk=name in primary_keys)

        column = self.entity.get_attribute(name)
        if is_fk:
            fk_info = self._get_fk_info(column)
            info.update(fk_info)

        validator = validator_services.try_get_validator(self.entity, column)
        if validator is not None:
            info.update(validator.get_info(for_update))

        return info

    def _validate_duplicate_data_fields(self, writable_fields, readable_fields=None):
        """
        validates that provided field names do not have overlap with extra data field names.

        :param tuple[str] writable_fields: writable field names.
        :param tuple[str] readable_fields: readable field names.

        :raises ExtraDataFieldsAndEntityFieldsOverlapError: extra data fields and
                                                            entity fields overlap error.
        """

        if not self.extra_data_fields:
            return

        fields = set(writable_fields).union(set(readable_fields or []))
        extra_fields = set(self.extra_data_fields)
        duplicates = fields.intersection(extra_fields)
        if duplicates:
            raise ExtraDataFieldsAndEntityFieldsOverlapError('These extra data fields have the '
                                                             'same name with entity [{entity}] '
                                                             'fields. please rename these extra '
                                                             'data fields in admin [{admin}] '
                                                             'class: {fields}'
                                                             .format(entity=self.entity,
                                                                     admin=self,
                                                                     fields=list(duplicates)))

    def _get_data_fields(self, writable_fields, for_update,
                         primary_keys, foreign_keys,
                         readable_fields=None):
        """
        gets all data fields of this admin page for specified operation.

        :param tuple[str] writable_fields: writable field names.
        :param bool for_update: specifies that fields must be returned for which operation.
        :param tuple[str] primary_keys: all primary key names.
        :param tuple[str] foreign_keys: all foreign key names.
        :param tuple[str] readable_fields: readable field names.

        :rtype: tuple[dict]
        """

        self._validate_duplicate_data_fields(writable_fields, readable_fields)
        fields = []
        for name in writable_fields:
            item = self._get_data_field(name, for_update, primary_keys, foreign_keys)
            item.setdefault('required', False)
            fields.append(item)

        extra_fields = self._get_extra_data_fields(for_update)
        fields.extend(extra_fields)
        fields = dict_utils.extended_sort(fields, 'required', reverse=True)

        if readable_fields:
            for name in readable_fields:
                if name not in writable_fields and name not in primary_keys:
                    item = self._get_data_field(name, for_update, primary_keys, foreign_keys)
                    item.update(read_only=True)
                    fields.append(item)

        return tuple(fields)

    @fast_cache
    def _get_create_fields(self):
        """
        gets all fields which should be used for create page.

        :rtype: tuple[dict]
        """

        writable_columns = self.entity.writable_primary_key_columns + \
            self.entity.writable_foreign_key_columns + self.entity.writable_columns

        return self._get_data_fields(writable_columns, False,
                                     self.entity.primary_key_columns,
                                     self.entity.foreign_key_columns)

    @fast_cache
    def _get_create_fields_dict(self):
        """
        gets all fields which should be used for create page as a dict.

        :rtype: dict
        """

        result = dict()
        fields = self._get_create_fields()
        for item in fields:
            result[item.get('field')] = item

        return result

    @fast_cache
    def _get_update_fields(self):
        """
        gets all fields which should be used for update page.

        :rtype: tuple[dict]
        """

        writable_columns = self.entity.writable_primary_key_columns + \
            self.entity.writable_foreign_key_columns + self.entity.writable_columns

        readable_columns = self.entity.readable_primary_key_columns + \
            self.entity.readable_foreign_key_columns + self.entity.readable_columns

        return self._get_data_fields(writable_columns, True,
                                     self.entity.primary_key_columns,
                                     self.entity.foreign_key_columns,
                                     readable_columns)

    @fast_cache
    def _get_update_fields_dict(self):
        """
        gets all fields which should be used for update page as a dict.

        :rtype: dict
        """

        result = dict()
        fields = self._get_update_fields()
        for item in fields:
            result[item.get('field')] = item

        return result

    def _get_link_info(self, title, register_name, type_=None,
                       button_type=None, new_tab=True, **filters):
        """
        gets the required link info for given inputs.

        the result of this method must be returned by admin methods
        which want to render a link on client list view.
        the aforementioned methods must be decorated using `@link` decorator.

        :param str title: the title of the link.

        :param str | type[BaseEntity] register_name: the register name or the entity class of
                                                     the related admin class to view its list
                                                     page after clicking on this link.

        :param str type_: the link type.
                          if not provided defaults to `button`.
        :enum type_:
            BUTTON = 'button'
            LINK = 'link'

        :param str button_type: the link button type.
                                this is only used if the `type_` is `button`.
                                defaults to `outlined` if not provided.
        :enum button_type:
            CONTAINED = 'contained'
            OUTLINED = 'outlined'
            TEXT = 'text'

        :param bool new_tab: open this link in a new tab.
                             defaults to True if not provided.

        :param **filters: any query strings that must be passed to the related
                          page after clicking on this link.

        :raises AdminPageNotFoundError: admin page not found error.

        :returns: dict(str title,
                       str register_name,
                       str type,
                       str button_type,
                       bool new_tab,
                       dict filters)
        :rtype: dict
        """

        if not isinstance(register_name, str):
            register_name = admin_services.register_name_for(register_name)

        if type_ not in LinkTypeEnum:
            type_ = LinkTypeEnum.BUTTON

        if button_type not in ButtonTypeEnum:
            button_type = ButtonTypeEnum.OUTLINED

        return dict(title=title,
                    register_name=register_name,
                    type=type_,
                    button_type=button_type,
                    new_tab=new_tab,
                    filters=filters)

    @fast_cache
    def _get_common_metadata(self):
        """
        gets the common metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata['name'] = self.name
        metadata['plural_name'] = self.get_plural_name()
        metadata['register_name'] = self.get_register_name()
        metadata['category'] = self.get_category()
        metadata['configs'] = admin_services.get_configs()
        return metadata

    def get_entity(self):
        """
        gets the entity class of this admin page.

        :rtype: type[BaseEntity]
        """

        return self.entity

    @fast_cache
    def get_register_name(self):
        """
        gets the register name of this admin page.

        :rtype: str
        """

        return self.register_name.lower()

    @fast_cache
    def get_category(self):
        """
        gets the category of this admin page.

        :rtype: str
        """

        if self.category not in (None, '') and not self.category.isspace():
            return self.category.upper()

        package = path_utils.get_object_package_name(self)
        if package is not None:
            package = package.replace('_', ' ')
            return package.upper()

        return admin_services.get_default_category()

    @fast_cache
    def get_plural_name(self):
        """
        gets the plural name of this admin page.

        :rtype: str
        """

        return self.plural_name or string_utils.pluralize(self.name)

    def get_singular_name(self):
        """
        gets the singular name of this admin page.

        :rtype: str
        """

        return self.name

    def get(self, pk):
        """
        gets an entity with given primary key.

        :param object pk: primary key of entity to be get.

        :raises EntityNotFoundError: entity not found error.

        :rtype: pyrin.database.model.base.BaseEntity
        """

        validator_services.validate(self.entity, **self._get_primary_key_holder(pk))
        return self._get(pk)

    def find(self, **filters):
        """
        finds entities with given filters.

        :keyword **filters: all filters to be passed to related find service.

        :raises ListFieldRequiredError: list field required error.

        :rtype: list[ROW_RESULT]
        """

        self._validate_filters(filters)
        store = get_current_store()
        query = store.query(*self._get_selectable_fields())
        query = self._perform_joins(query)
        query = self._filter_query(query, **filters)
        query = self._perform_order_by(query, **filters)
        query = self._paginate_query(query, **filters)
        results = query.all()
        return self._process_find_results(results, **filters)

    @classmethod
    def create(cls, **data):
        """
        creates an entity with given data.

        it's preferred for this method to return the pk of created entity
        if it is not a composite primary key. this lets the client to fill
        fk fields automatically after create.

        :keyword **data: all data to be passed to related create service.

        :rtype: object
        """

        validator_services.validate_dict(cls.entity, data)
        cls._validate_extra_fields(data)
        if cls.create_service is not None:
            result = cls.create_service(**data)
            if cls._has_single_primary_key():
                return result
            return None
        else:
            return cls._create(**data)

    @classmethod
    def update(cls, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related update service.

        :raises EntityNotFoundError: entity not found error.
        """

        validator_services.validate(cls.entity, **cls._get_primary_key_holder(pk))
        validator_services.validate_dict(cls.entity, data, for_update=True)
        if cls.update_service is not None:
            cls.update_service(pk, **data)
        else:
            cls._update(pk, **data)

    @classmethod
    def remove(cls, pk):
        """
        deletes an entity with given pk.

        :param object pk: entity primary key to be deleted.
        """

        validator_services.validate(cls.entity, **cls._get_primary_key_holder(pk))
        if cls.remove_service is not None:
            cls.remove_service(pk)
        else:
            cls._remove(pk)

    def remove_bulk(self, pk):
        """
        deletes entities with given primary keys.

        :param object | list[object] pk: entity primary keys to be deleted.
        """

        pk = misc_utils.make_iterable(pk)
        for item in pk:
            validator_services.validate(self.entity, **self._get_primary_key_holder(item))

        self._remove_bulk(*pk)

    def remove_all(self):
        """
        deletes all entities.
        """

        self._remove_all()

    def call_method(self, name, argument):
        """
        calls the method with given name with given argument and returns the result.

        :param str name: method name.
        :param ROW_RESULT argument: the method argument.

        :raises InvalidMethodNameError: invalid method name error.

        :rtype: object
        """

        if name not in self.method_names:
            raise InvalidMethodNameError('Method [{method}] is not present in [{admin}] class.'
                                         .format(method=name, admin=self))

        method = getattr(self, name)
        return method(argument)

    def has_get_permission(self):
        """
        gets a value indicating that this admin page has get permission.

        note that entities with composite primary key does not support get.

        :rtype: bool
        """

        return self._has_single_primary_key() and self.get_permission

    def has_create_permission(self):
        """
        gets a value indicating that this admin page has create permission.

        :rtype: bool
        """

        return self.create_permission

    def has_update_permission(self):
        """
        gets a value indicating that this admin page has update permission.

        note that entities with composite primary key does not support update.

        :rtype: bool
        """

        return self._has_single_primary_key() and self.update_permission

    def has_remove_permission(self):
        """
        gets a value indicating that this admin page has single or bulk remove permission.

        note that entities with composite primary key does not support single or bulk remove.

        :rtype: bool
        """

        return self._has_single_primary_key() and self.remove_permission

    def has_remove_all_permission(self):
        """
        gets a value indicating that this admin page has remove all permission.

        :rtype: bool
        """

        return self.remove_all_permission

    @fast_cache
    def get_main_metadata(self):
        """
        gets the main metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata.update(self._get_common_metadata())
        metadata['has_create_permission'] = self.has_create_permission()
        return metadata

    @fast_cache
    def get_find_metadata(self):
        """
        gets the find metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata.update(self._get_common_metadata())
        metadata['datasource_info'] = self._get_list_datasource_info()
        metadata['field_names'] = self._get_list_field_names()
        metadata['sortable_fields'] = self._get_sortable_fields()
        metadata['has_create_permission'] = self.has_create_permission()
        metadata['has_remove_permission'] = self.has_remove_permission()
        metadata['has_remove_all_permission'] = self.has_remove_all_permission()
        metadata['has_get_permission'] = self.has_get_permission()
        metadata['paged'] = self.list_paged
        metadata['page_size'] = self._get_page_size()
        metadata['max_page_size'] = self._get_max_page_size()
        metadata['page_size_options'] = self._get_page_size_options()
        metadata['table_type'] = self.list_table_type
        metadata['pagination_type'] = self.list_pagination_type
        metadata['pagination_position'] = self.list_pagination_position
        metadata['enable_export'] = self.list_enable_export
        metadata['export_name'] = self._get_list_export_name()
        metadata['link_pk'] = self.list_link_pk
        metadata['link_fk'] = self.list_link_fk
        metadata['column_selection'] = self.list_column_selection
        metadata['column_ordering'] = self.list_column_ordering
        metadata['grouping'] = self.list_grouping
        metadata['search'] = self.list_search
        metadata['search_debounce_interval'] = self.list_search_debounce_interval
        metadata['datetime_format'] = self.list_datetime_format
        metadata['date_format'] = self.list_date_format
        metadata['time_format'] = self.list_time_format
        metadata['locale'] = self.list_locale
        metadata['max_body_height'] = self.list_max_body_height
        return metadata

    @fast_cache
    def get_create_metadata(self):
        """
        gets the create metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata.update(self._get_common_metadata())
        metadata['has_create_permission'] = self.has_create_permission()
        metadata['data_fields'] = self._get_create_fields()
        metadata['data_fields_dict'] = self._get_create_fields_dict()
        return metadata

    @fast_cache
    def get_update_metadata(self):
        """
        gets the update metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata.update(self._get_common_metadata())
        metadata['has_update_permission'] = self.has_update_permission()
        metadata['has_get_permission'] = self.has_get_permission()
        metadata['has_remove_permission'] = self.has_remove_permission()
        metadata['data_fields'] = self._get_update_fields()
        metadata['data_fields_dict'] = self._get_update_fields_dict()
        return metadata

    def populate_caches(self):
        """
        populates required caches of this admin page.
        """

        self.get_main_metadata()
        self.get_find_metadata()
        self.get_create_metadata()
        self.get_update_metadata()
        self._get_list_search_fields_to_column_map()
        self._get_primary_keys()
        self._get_default_list_fields()
        self._get_list_entities()
        self._get_list_labels()

    @property
    def method_names(self):
        """
        gets the list of all method names of this admin page to be used for result processing.

        :rtype: tuple[str]
        """

        return self._method_names
