# -*- coding: utf-8 -*-
"""
admin page base module.
"""

import inspect

import pyrin.filtering.services as filtering_services
import pyrin.validator.services as validator_services
import pyrin.security.session.services as session_services

from pyrin.admin.interface import AbstractAdminPage
from pyrin.admin.page.schema import AdminSchema
from pyrin.core.globals import SECURE_TRUE, SECURE_FALSE
from pyrin.admin.page.mixin import AdminPageCacheMixin
from pyrin.caching.mixin.decorators import fast_cache
from pyrin.database.services import get_current_store
from pyrin.database.model.base import BaseEntity
from pyrin.admin.page.exceptions import InvalidListFieldError, ListFieldRequiredError, \
    InvalidMethodNameError, InvalidAdminEntityTypeError, AdminNameRequiredError, \
    AdminRegisterNameRequiredError


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

    # name of this admin page for representation.
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
    list_pk = True

    # specifies that if 'list_fields' are not provided also show fk columns in list view.
    list_fk = True

    # specifies that if 'list_fields' are not provided also show expression
    # level hybrid property columns in list view.
    list_expression_level_hybrid_properties = True

    # list of default ordering columns.
    # it must be string names. for example: ('first_name', '-last_name')
    list_ordering = ()

    # show the total count of records in list view.
    list_total_count = True

    # specifies that each row must have an index in it.
    list_indexed = False

    # list index name to be added to each row.
    list_index_name = None

    # start index of rows.
    list_start_index = 1

    # columns to show in list filter.
    list_filters = ()

    # max records per page
    list_per_page = 100

    # max records to fetch on show all.
    list_max_show_all = 200

    # ===================== VALIDATION CONFIGS ===================== #

    # specifies that filters must be validated on find.
    validate_for_find = True

    # specifies that inputs must be validated on create.
    validate_for_create = True

    # specifies that inputs must be validated on update.
    validate_for_update = True

    # specifies that inputs must be validated on remove.
    validate_for_remove = True

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

    # ===================== OTHER CONFIGS ===================== #

    # the category name to register this admin page in it.
    # all admin pages with the same category will be grouped together.
    # the category name is case-insensitive.
    category = None

    # plural name of this admin page for representation.
    plural_name = None

    # column names to be used in search bar.
    search_fields = ()

    # related columns that need to open a separate form to be selected.
    raw_id_fields = ()

    # columns that are readonly in edit form.
    readonly_fields = ()

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

    def __populate_caches(self):
        """
        populates all caches of this admin page.
        """

        self._get_list_field_names()
        self._get_list_temp_field_names()
        self._get_default_list_fields()
        self._get_list_fields()
        self._get_list_temp_fields()
        self._get_selectable_fields()
        self._extract_method_names()

    @fast_cache
    def _get_primary_key_name(self):
        """
        gets the name of the primary key of this admin page's related entity.

        note that if the entity has a composite primary key, this method returns None.

        :rtype: str
        """

        if len(self.entity.primary_key_columns) == 1:
            return self.entity.primary_key_columns[0]

        return None

    def _get_primary_key_holder(self, pk):
        """
        gets a dict with the primary key name of this page's entity set to the given value.

        :param object pk: value to be set to primary key.

        :rtype: dict
        """

        pk_name = self._get_primary_key_name()
        pk_holder = dict()
        pk_holder[pk_name] = pk

        return pk_holder

    def _show_total_count(self):
        """
        gets a value indicating that total count must be shown on list view.

        :returns: SECURE_TRUE | SECURE_FALSE
        """

        if self.list_total_count is True:
            return SECURE_TRUE

        return SECURE_FALSE

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

    @fast_cache
    def _extract_method_names(self):
        """
        extracts all valid method names from list fields.

        :rtype: tuple[str]
        """

        names = []
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

        :rtype: tuple[str]
        """

        all_fields = ()
        if not self.list_fields:
            all_fields = self._get_default_list_fields()
        else:
            all_fields = self.list_fields

        return self._extract_field_names(all_fields, allow_string=True)

    @fast_cache
    def _get_list_temp_field_names(self):
        """
        gets all list temp field names of this admin page.

        :raises InvalidListFieldError: invalid list field error.

        :rtype: tuple[str]
        """

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
        return tuple(results)

    @fast_cache
    def _get_list_temp_fields(self):
        """
        gets all fields from `list_temp_fields`.

        :rtype: tuple
        """

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

        filters.setdefault('order_by', self.list_ordering)
        return query.safe_order_by(self.entity,
                                   *self.entity.primary_key_columns,
                                   **filters)

    def _paginate_query(self, query, **filters):
        """
        paginates given query and returns a new query object.

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

        return query.paginate(inject_total=self._show_total_count(), **filters)

    def _process_find_results(self, results, **options):
        """
        processes the given results and returns a list of serialized values.

        :param list[ROW_RESULT] results: results to be processed.

        :rtype: list[dict]
        """

        paginator = session_services.get_request_context('paginator')
        return self._schema.filter(results, paginator=paginator)

    def get_entity(self):
        """
        gets the entity class of this admin page.

        :rtype: BaseEntity
        """

        return self.entity

    def get_register_name(self):
        """
        gets the register name of this admin page.

        :rtype: str
        """

        return self.register_name.lower()

    def get_category(self):
        """
        gets the category of this admin page.

        it may return None if no category is set for this admin page.

        :rtype: str
        """

        if self.category not in (None, ''):
            return self.category.upper()

        return None

    def find(self, **filters):
        """
        finds entities with given filters.

        :keyword **filters: all filters to be passed to related find service.

        :raises ListFieldRequiredError: list field required error.

        :rtype: list[ROW_RESULT]
        """

        if self.validate_for_find:
            self._validate_filters(filters)

        store = get_current_store()
        query = store.query(*self._get_selectable_fields())
        query = self._perform_joins(query)
        query = self._filter_query(query, **filters)
        query = self._perform_order_by(query, **filters)
        query = self._paginate_query(query, **filters)
        results = query.all()
        return self._process_find_results(results, **filters)

    def _create(self, **data):
        """
        creates an entity with given data.

        :keyword **data: all data to be passed to related create service.
        """

        entity = self.entity(**data)
        entity.save()

    def create(self, **data):
        """
        creates an entity with given data.

        :keyword **data: all data to be passed to related create service.
        """

        if self.validate_for_create:
            validator_services.validate_dict(self.entity, data)

        if self.create_service is not None:
            self.create_service(**data)
        else:
            self._create(**data)

    def _update(self, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related update service.
        """

        store = get_current_store()
        entity = store.query(self.entity).get(pk)
        entity.update(**data)

    def update(self, pk, **data):
        """
        updates an entity with given data.

        :param object pk: entity primary key to be updated.

        :keyword **data: all data to be passed to related update service.
        """

        if self.validate_for_update:
            validator_services.validate(self.entity, **self._get_primary_key_holder(pk))
            validator_services.validate_dict(self.entity, data, for_update=True)

        if self.update_service is not None:
            self.update_service(pk, **data)
        else:
            self._update(pk, **data)

    def _remove(self, pk):
        """
        deletes an entity with given pk.

        :param object pk: entity primary key to be deleted.
        """

        store = get_current_store()
        pk_name = self._get_primary_key_name()
        pk_column = self.entity.get_attribute(pk_name)
        store.query(self.entity).filter(pk_column == pk).delete()

    def remove(self, pk):
        """
        deletes an entity with given pk.

        :param object pk: entity primary key to be deleted.
        """

        if self.validate_for_remove:
            validator_services.validate(self.entity, **self._get_primary_key_holder(pk))

        if self.remove_service is not None:
            self.remove_service(pk)
        else:
            self._remove(pk)

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

    @property
    def method_names(self):
        """
        gets the list of all method names of this admin page to be used for result processing.

        :rtype: tuple[str]
        """

        return self._method_names
