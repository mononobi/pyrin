# -*- coding: utf-8 -*-
"""
users internal manager module.
"""

import pyrin.security.services as security_services
import pyrin.validator.services as validator_services
import pyrin.security.hashing.services as hashing_services
import pyrin.globalization.datetime.services as datetime_services

from pyrin.core.globals import _
from pyrin.core.structs import Manager
from pyrin.users.internal import InternalUsersPackage
from pyrin.users.internal.models import InternalUserEntity
from pyrin.database.services import get_current_store
from pyrin.users.internal.exceptions import InternalUserNotFoundError, PasswordsDoNotMatchError


class InternalUsersManager(Manager):
    """
    internal users manager class.
    """

    package_class = InternalUsersPackage

    def _get(self, id, **options):
        """
        gets the specified internal user.

        :param int id: internal user id to get its info.

        :raises InternalUserNotFoundError: internal user not found error.

        :rtype: InternalUserEntity
        """

        data = validator_services.validate(InternalUserEntity, id=id)
        store = get_current_store()
        user = store.query(InternalUserEntity).get(data.id)

        if user is None:
            raise InternalUserNotFoundError(_('Internal user [{user_id}] not found.')
                                            .format(user_id=data.id))

        return user

    def _validate_passwords(self, password, confirm_password):
        """
        validates that given passwords are match.

        :param str password: password.
        :param str confirm_password: confirm password.

        :raises PasswordsDoNotMatchError: passwords do not match error.
        """

        if password != confirm_password:
            message = _('Provided passwords do not match')
            raise PasswordsDoNotMatchError(f'{message}.',
                                           data=dict(password=message,
                                                     confirm_password=message))

    def get(self, id, *columns, **options):
        """
        gets the internal user with given id.

        :param int id: internal user id to be get.

        :param CoreColumn columns: columns to be fetched.
                                   if not provided all columns will be fetched.

        :raises InternalUserNotFoundError: internal user not found error.

        :rtype: InternalUserEntity | ROW_RESULT
        """

        if not columns:
            return self._get(id, **options)

        data = validator_services.validate(InternalUserEntity, id=id)
        store = get_current_store()
        user = store.query(*columns).filter(InternalUserEntity.id == data.id).one_or_none()
        if user is None:
            raise InternalUserNotFoundError(_('Internal user [{user_id}] not found.')
                                            .format(user_id=data.id))

        return user

    def is_active(self, id, **options):
        """
        gets a value indicating that given internal user is active.

        :param int id: internal user id to check its active status.

        :raises InternalUserNotFoundError: internal user not found error.

        :rtype: bool
        """

        entity = self.get(id, InternalUserEntity.is_active, **options)
        return entity.is_active

    def create(self, username, password, confirm_password,
               first_name, last_name, **options):
        """
        creates a new internal user based on given inputs.

        :param str username: username.
        :param str password: password.
        :param str confirm_password: confirm password.
        :param str first_name: first name.
        :param str last_name: last name.

        :keyword str mobile: mobile number.
        :keyword str email: email address.
        :keyword int gender: gender.
        :enum gender:
            FEMALE = 0
            MALE = 1
            OTHER = 2

        :keyword bool is_active: is active user.
        :keyword bool is_superuser: is superuser.

        :raises PasswordsDoNotMatchError: passwords do not match error.
        """

        options.update(username=username, password=password,
                       confirm_password=confirm_password,
                       first_name=first_name, last_name=last_name)
        validator_services.validate_dict(InternalUserEntity, options)
        password = options.get('password')
        confirm_password = options.get('confirm_password')
        self._validate_passwords(password, confirm_password)
        entity = InternalUserEntity(**options)
        entity.password_hash = security_services.get_password_hash(password)
        entity.save()

    def update(self, id, **options):
        """
        updates the given internal user based on given inputs.

        :param int id: internal user id.

        :keyword str username: username.
        :keyword str password: password.
        :keyword str confirm_password: confirm password.
        :keyword str first_name: first name.
        :keyword str last_name: last name.
        :keyword str mobile: mobile number.
        :keyword str email: email address.
        :keyword int gender: gender.
        :enum gender:
            FEMALE = 0
            MALE = 1
            OTHER = 2

        :keyword bool is_active: is active user.
        :keyword bool is_superuser: is superuser.

        :raises PasswordsDoNotMatchError: passwords do not match error.
        """

        entity = self._get(id)
        validator_services.validate_dict(InternalUserEntity, options, for_update=True)
        password = options.get('password')
        confirm_password = options.get('confirm_password')
        if password is not None or confirm_password is not None:
            self._validate_passwords(password, confirm_password)
            entity.password_hash = security_services.get_password_hash(password)

        entity.update(**options)

    def get_login_user(self, username, password, *columns, **options):
        """
        gets an internal user with given username and password for logging in.

        it may return None if no internal user found.

        :param str username: username.
        :param str password: password.

        :param CoreColumn columns: columns to be fetched.
                                   if not provided all columns will be fetched.

        :rtype: InternalUserEntity | ROW_RESULT
        """

        columns = list(columns)
        if not columns:
            columns = [InternalUserEntity]
        elif InternalUserEntity.password_hash not in columns:
            columns.append(InternalUserEntity.password_hash)

        store = get_current_store()
        user = store.query(*columns)\
            .filter(InternalUserEntity.username == username).one_or_none()

        if user is None or hashing_services.is_match(password, user.password_hash) is not True:
            return None

        return user

    def update_last_login_at(self, id, **options):
        """
        updates the last login at for given user to current datetime.

        :param int id: internal user id to update its last login at.

        :raises InternalUserNotFoundError: internal user not found error.
        """

        store = get_current_store()
        count = store.query(InternalUserEntity).filter(InternalUserEntity.id == id)\
            .update({InternalUserEntity.last_login_at: datetime_services.now()})

        if count <= 0:
            raise InternalUserNotFoundError(_('Internal user [{user_id}] not found.')
                                            .format(user_id=id))
