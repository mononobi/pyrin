# -*- coding: utf-8 -*-
"""
admin page base module.
"""

import inspect

from sqlalchemy.sql.elements import Label
from sqlalchemy.orm import InstrumentedAttribute

import pyrin.admin.services as admin_services
import pyrin.filtering.services as filtering_services
import pyrin.validator.services as validator_services
import pyrin.security.session.services as session_services
import pyrin.database.model.services as model_services
import pyrin.configuration.services as config_services
import pyrin.database.paging.services as paging_services
import pyrin.utils.path as path_utils
import pyrin.utils.string as string_utils
import pyrin.utils.sqlalchemy as sqla_utils
import pyrin.utils.misc as misc_utils

from pyrin.core.globals import _
from pyrin.core.structs import SecureList
from pyrin.admin.interface import AbstractAdminPage
from pyrin.admin.enumerations import TableTypeEnum
from pyrin.admin.page.schema import AdminSchema
from pyrin.core.globals import SECURE_TRUE
from pyrin.admin.page.mixin import AdminPageCacheMixin
from pyrin.caching.mixin.decorators import fast_cache
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.paging.paginator import SimplePaginator
from pyrin.database.services import get_current_store
from pyrin.database.model.base import BaseEntity
from pyrin.security.session.enumerations import RequestContextEnum
from pyrin.admin.page.exceptions import InvalidListFieldError, ListFieldRequiredError, \
    InvalidMethodNameError, InvalidAdminEntityTypeError, AdminNameRequiredError, \
    AdminRegisterNameRequiredError, RequiredValuesNotProvidedError, \
    CompositePrimaryKeysNotSupportedError, ColumnIsNotForeignKeyError, \
    DuplicateListFieldNamesError


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

    # specifies that if 'list_fields' are not provided only show readable
    # columns of the entity in list view.
    list_only_readable = True

    # specifies that if 'list_fields' are not provided also show pk columns in list view.
    # note that if the admin page has get permission, pk columns will be always added.
    list_pk = True

    # specifies that if 'list_fields' are not provided also show fk columns in list view.
    list_fk = True

    # specifies that if 'list_fields' are not provided also show expression
    # level hybrid property columns in list view.
    list_expression_level_hybrid_properties = True

    # list of default ordering columns.
    # it must be string names from `list_fields` or `list_temp_fields`.
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

    # a value to be shown when the relevant data is null.
    list_null_value = '-'

    # a dict containing field names and their client type for fields which their
    # type could not be detected automatically. for example hybrid property fields
    # or fields which their value is coming from a method of this admin page.
    # note that the provided types must be from 'ClientTypeEnum' values.
    # for example: {'is_viewed': ClientTypeEnum.BOOLEAN}
    list_extra_field_types = {}

    # a value to define client-side table type.
    # it should be from 'TableTypeEnum' values.
    list_table_type = TableTypeEnum.DENSE

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

    # specifies that this admin page has remove permission.
    # note that if entity has composite primary key, it does not
    # have remove permission and this value will be ignored.
    remove_permission = True

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
    # [str field_name]
    # for example:
    # ['password', 'age', 'join_date']
    # if the provided names do not have related validators, the
    # type of their values will be considered as string.
    extra_data_fields = ()

    # column names to be used in search bar.
    search_fields = ()

    # columns that are readonly in edit form.
    readonly_fields = ()

    # ===================== INTERNAL CONFIGS ===================== #

    # paginator class to be used.
    paginator_class = SimplePaginator

    # the fully qualified name of find api.
    FIND_ENDPOINT = 'pyrin.admin.api.find'

    # a name to be used to return primary key column to client as a hidden column.
    # this is required if the current admin page has any of get or remove permissions.
    HIDDEN_PK_NAME = '__pk__'

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

        self.__populate_caches()
        # list of method names of this admin page to be used for processing the results.
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

    def __populate_caches(self):
        """
        populates required caches of this admin page.
        """

        self._get_list_field_names()
        self._get_list_temp_field_names()
        self._get_selectable_fields()

    def _get_column_title(self, name):
        """
        gets the column title for given field name for list page.

        :param str name: field name.

        :rtype: str
        """

        name = name.replace('_', ' ')
        return name.upper()

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

        it returns True if this admin page has any of `get`, `update` or `remove` permissions.

        :rtype: bool
        """

        return self.has_get_permission() or \
            self.has_remove_permission() or self.has_update_permission()

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

        if len(all_fields) != len(set(all_fields)):
            raise DuplicateListFieldNamesError('There are some duplicate field names '
                                               'in "list_fields" of [{admin}] class. '
                                               'this will make the find result incorrect. '
                                               'please remove duplicate fields or set '
                                               'unique labels for them.'.format(admin=self))

        return all_fields

    def _get_relevant_column(self, name):
        """
        gets the relevant column attribute of given field name.

        it may return None if no related column found in `list_fields`.

        :param str name: field name.

        :rtype: sqlalchemy.orm.InstrumentedAttribute
        """

        selectable_fields = self._get_list_fields()
        for item in selectable_fields:
            if self._is_valid_field(item) and item.key == name:
                if isinstance(item, InstrumentedAttribute):
                    return item
                elif isinstance(item, Label) and item.base_columns:
                    columns = list(item.base_columns)
                    if isinstance(columns[0], CoreColumn):
                        return model_services.get_instrumented_attribute(columns[0])
                break

        return None

    @fast_cache
    def _get_list_fields_to_column_map(self):
        """
        gets a dict of all list field names and their related columns.

        the column value may be None if the name does not belong to a column.
        for example method names or hybrid properties.

        :returns: dict(InstrumentAttribute name)
        :rtype: dict
        """

        result = dict()
        all_fields = self._get_list_field_names()
        for name in all_fields:
            attribute = self._get_relevant_column(name)
            result[name] = attribute

        return result

    def _get_pk_info(self, column):
        """
        gets a dict containing pk info for given column if required.

        :param InstrumentedAttribute column: column to be checked.

        :returns: dict(bool is_pk,
                       str pk_register_name)
        :rtype: dict
        """

        result = dict(is_pk=False, pk_register_name=None)
        if not column.property or not column.property.columns:
            return result

        base_column = column.property.columns[0]
        is_pk = base_column.primary_key
        if is_pk is True:
            admin_page = admin_services.try_get_admin_page(column.class_)
            if admin_page is not None and admin_page.has_get_permission() is True:
                result.update(is_pk=is_pk, pk_register_name=admin_page.get_register_name())

        return result

    def _get_fk_info(self, column):
        """
        gets a dict containing fk info for given column if required.

        :param InstrumentedAttribute column: column to be checked.

        :returns: dict(bool is_fk,
                       str fk_register_name)
        :rtype: dict
        """

        result = dict(is_fk=False, fk_register_name=None)
        if not column.property or not column.property.columns:
            return result

        base_column = column.property.columns[0]
        is_fk = base_column.is_foreign_key
        if is_fk is True:
            admin_page = admin_services.try_get_admin_page(column.class_)
            if admin_page is not None and admin_page.has_get_permission() is True:
                result.update(is_fk=is_fk, fk_register_name=admin_page.get_register_name())

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
                type_ = admin_services.get_client_type(info.get('client_type'),
                                                       info.get('client_format'))
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

        :returns: tuple[dict(str title: field title,
                             str field: field name to be used for data binding)]

        :rtype: tuple[dict]
        """

        results = []
        all_fields = self._get_list_field_names()
        sortable_fields = self._get_sortable_fields()
        for item in all_fields:
            info = dict(field=item,
                        title=self._get_column_title(item),
                        sorting=item in sortable_fields,
                        emptyValue=self.list_null_value)

            if item == self.HIDDEN_PK_NAME:
                info.update(hidden=True)
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
        fields.append(primary_key.label(self.HIDDEN_PK_NAME))

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
            expression_level_hybrid_properties.append(
                self.entity.get_attribute(hybrid_property))

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

        results = [item for item in self.list_fields if self._is_valid_field(item)]
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
        provide columns of other entities in `list_fields` too.

        :param CoreQuery query: query instance.

        :rtype: CoreQuery
        """

        return query

    def _filter_query(self, query, **filters):
        """
        filters given query and returns a new query object.

        :param CoreQuery query: query instance.

        :rtype: CoreQuery
        """

        expressions = filtering_services.filter(self.entity, filters)
        return query.filter(*expressions)

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

    def _has_single_primary_key(self):
        """
        gets a value indicating that the related entity has a single primary key.

        :rtype: bool
        """

        return len(self.entity.primary_key_columns) == 1

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

        :keyword **data: all data to be passed to create method.
        """

        entity = cls.entity(**data)
        cls._process_created_entity(entity, **data)
        entity.save()

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
    def _update(cls, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to update method.
        """

        store = get_current_store()
        entity = store.query(cls.entity).get(pk)
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

    def _remove_all(self, *pk):
        """
        deletes all entities with given primary keys.

        :param object pk: entity primary key to be deleted.
        """

        store = get_current_store()
        pk_name = self._get_primary_key_name()
        pk_column = self.entity.get_attribute(pk_name)
        store.query(self.entity).filter(pk_column.in_(pk)).delete()

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
            if isinstance(item, Label):
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
                    and item.key != self.HIDDEN_PK_NAME:
                results.append(item.key)

        return tuple(set(results))

    def _get_fk_url(self, name):
        """
        gets the fk url for given attribute name.

        it may return None if the fk entity does not have an admin page.

        :param str name: attribute name of entity.

        :raises ColumnIsNotForeignKeyError: column is not foreign key error.

        :rtype: str
        """

        if name not in self.entity.foreign_key_columns:
            raise ColumnIsNotForeignKeyError('Provided column [{name}] is not a '
                                             'foreign key of [{entity}] class.'
                                             .format(name=name, entity=self.entity))

        attribute = self.entity.get_attribute(name)
        foreign_keys = list(attribute.property.columns[0].foreign_keys)
        entity = sqla_utils.get_class_by_table(model_services.get_declarative_base(),
                                               foreign_keys[0].constraint.referred_table,
                                               raise_multi=False)

        admin_page = admin_services.try_get_admin_page(entity)
        if admin_page is not None:
            return admin_services.url_for(admin_page.get_register_name())

        return None

    @fast_cache
    def _get_data_fields(self):
        """
        gets all data fields of this admin page.

        :rtype: tuple[dict]
        """

        fields = []
        writable_columns = self.entity.writable_primary_key_columns + \
            self.entity.writable_foreign_key_columns + self.entity.writable_columns

        for name in writable_columns:
            is_fk = name in self.entity.writable_foreign_key_columns
            item = dict(name=name, is_fk=is_fk,
                        is_pk=name in self.entity.writable_primary_key_columns)

            if is_fk:
                item.update(fk_url=self._get_fk_url(name))

            validator = validator_services.try_get_validator(self.entity,
                                                             self.entity.get_attribute(name))
            if validator is not None:
                item.update(validator.get_info())

            fields.append(item)

        if self.extra_data_fields:
            for name in self.extra_data_fields:
                item = dict(name=name, is_fk=False, is_pk=False)
                validator = validator_services.try_get_validator(self.entity, name)
                if validator is not None:
                    item.update(validator.get_info())

                fields.append(item)

        return tuple(fields)

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

        if self.category not in (None, ''):
            return self.category.upper()

        package = path_utils.get_object_package_name(self)
        if package is not None:
            return package.upper()

        return admin_services.get_default_category()

    @fast_cache
    def get_plural_name(self):
        """
        gets the plural name of this admin page.

        :rtype: str
        """

        return self.plural_name or string_utils.pluralize(self.name)

    def get(self, pk):
        """
        gets an entity with given primary key.

        :param object pk: primary key of entity to be get.

        :rtype: pyrin.database.model.base.BaseEntity
        """

        validator_services.validate(self.entity, **self._get_primary_key_holder(pk))
        store = get_current_store()
        entity = store.query(self.entity).get(pk)
        return entity

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

        :keyword **data: all data to be passed to related create service.
        """

        validator_services.validate_dict(cls.entity, data)
        cls._validate_extra_fields(data)
        if cls.create_service is not None:
            cls.create_service(**data)
        else:
            cls._create(**data)

    @classmethod
    def update(cls, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related update service.
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

    def remove_all(self, pk):
        """
        deletes entities with given primary keys.

        :param object | list[object] pk: entity primary keys to be deleted.
        """

        pk = misc_utils.make_iterable(pk)
        for item in pk:
            validator_services.validate(self.entity, **self._get_primary_key_holder(item))

        self._remove_all(*pk)

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
        gets a value indicating that this admin page has remove permission.

        note that entities with composite primary key does not support remove.

        :rtype: bool
        """

        return self._has_single_primary_key() and self.remove_permission

    @fast_cache
    def get_main_metadata(self):
        """
        gets the main metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata['name'] = self.name
        metadata['plural_name'] = self.get_plural_name()
        metadata['register_name'] = self.get_register_name()
        metadata['category'] = self.get_category()
        metadata['has_create_permission'] = self.has_create_permission()
        return metadata

    @fast_cache
    def get_find_metadata(self):
        """
        gets the find metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata['register_name'] = self.get_register_name()
        metadata['name'] = self.name
        metadata['plural_name'] = self.get_plural_name()
        metadata['category'] = self.get_category()
        metadata['datasource_info'] = self._get_list_datasource_info()
        metadata['sortable_fields'] = self._get_sortable_fields()
        metadata['has_create_permission'] = self.has_create_permission()
        metadata['has_remove_permission'] = self.has_remove_permission()
        metadata['has_get_permission'] = self.has_get_permission()
        metadata['pk_name'] = self.HIDDEN_PK_NAME
        metadata['paged'] = self.list_paged
        metadata['page_size'] = self._get_page_size()
        metadata['max_page_size'] = self._get_max_page_size()
        metadata['page_size_options'] = self._get_page_size_options()
        metadata['table_type'] = self.list_table_type
        return metadata

    @fast_cache
    def get_create_metadata(self):
        """
        gets the create metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata['register_name'] = self.get_register_name()
        metadata['name'] = self.name
        metadata['plural_name'] = self.get_plural_name()
        metadata['category'] = self.get_category()
        metadata['has_create_permission'] = self.has_create_permission()
        metadata['url'] = admin_services.url_for(self.get_register_name())
        metadata['data_fields'] = self._get_data_fields()
        return metadata

    @fast_cache
    def get_update_metadata(self):
        """
        gets the update metadata of this admin page.

        :rtype: dict
        """

        metadata = dict()
        metadata['register_name'] = self.get_register_name()
        metadata['name'] = self.name
        metadata['plural_name'] = self.get_plural_name()
        metadata['category'] = self.get_category()
        metadata['has_update_permission'] = self.has_update_permission()
        metadata['has_get_permission'] = self.has_get_permission()
        metadata['has_remove_permission'] = self.has_remove_permission()
        metadata['url'] = admin_services.url_for(self.get_register_name())
        metadata['data_fields'] = self._get_data_fields()
        return metadata

    @property
    def method_names(self):
        """
        gets the list of all method names of this admin page to be used for result processing.

        :rtype: tuple[str]
        """

        return self._method_names
