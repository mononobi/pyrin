# -*- coding: utf-8 -*-
"""
admin users manager module.
"""

import pyrin.security.services as security_services
import pyrin.validator.services as validator_services

from pyrin.core.globals import _
from pyrin.admin.users.models import AdminUserEntity
from pyrin.database.services import get_current_store
from pyrin.security.users.manager import UsersManager as BaseUsersManager
from pyrin.admin.users.exceptions import AdminUserNotFoundError, PasswordsDoNotMatchError


class AdminUsersManager(BaseUsersManager):
    """
    admin users manager class.
    """

    def _get(self, id, **options):
        """
        gets the specified admin user.

        :param int id: admin user id to get its info.

        :raises AdminUserNotFoundError: admin user not found error.

        :rtype: AdminUserEntity
        """

        data = validator_services.validate(AdminUserEntity, id=id)
        store = get_current_store()
        user = store.query(AdminUserEntity).get(data.id)

        if user is None:
            raise AdminUserNotFoundError(_('Admin user [{user_id}] not found.')
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

    def is_active(self, user, **options):
        """
        gets a value indicating that given admin user is active.

        :param int user: admin user to check its active status.

        :raises AdminUserNotFoundError: admin user not found error.

        :rtype: bool
        """

        entity = self._get(user, **options)
        return entity.is_active

    def create(self, username, password, confirm_password,
               first_name, last_name, **options):
        """
        creates a new admin user based on given inputs.

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
        validator_services.validate_dict(AdminUserEntity, options)
        password = options.get('password')
        confirm_password = options.get('confirm_password')
        self._validate_passwords(password, confirm_password)
        entity = AdminUserEntity(**options)
        entity.password_hash = security_services.get_password_hash(password)
        entity.save()

    def update(self, id, **options):
        """
        updates the given admin user based on given inputs.

        :param int id: admin user id.

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
        validator_services.validate_dict(AdminUserEntity, options, for_update=True)
        password = options.get('password')
        confirm_password = options.get('confirm_password')
        if password is not None or confirm_password is not None:
            self._validate_passwords(password, confirm_password)
            entity.password_hash = security_services.get_password_hash(password)

        entity.update(**options)
