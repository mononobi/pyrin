# -*- coding: utf-8 -*-
"""
pyrin release manager.
"""

import io
import re
import subprocess

import fire


class ReleaseManager:
    """
    release manager class.
    """

    PYRIN_VERSION_FILE = '../../src/pyrin/__init__.py'
    DEFAULT_CHANGE = 'patch'
    DEFAULT_IS_BETA = True

    @classmethod
    def _get_current_version(cls):
        """
        gets current pyrin version from pyrin package.

        :returns: tuple(int major, int minor, int patch, str beta)
        :rtype: tuple
        """

        with io.open(cls.PYRIN_VERSION_FILE, 'rt', encoding='utf8') as version_file:
            version = re.search(r"__version__ = '(.*?)'", version_file.read()).group(1)

        parts = version.split('.')
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])

        beta = None
        if len(parts) > 3:
            beta = parts[3]

        return major, minor, patch, beta

    @classmethod
    def _format_version(cls, version):
        """
        formats the given version.

        :param tuple version: version to be formatted.
        :type version: tuple(int major, int minor, int patch, str beta)

        :rtype: str
        """

        major, minor, patch, beta = version
        parts = [str(major), str(minor), str(patch)]

        if beta is not None:
            parts.append(str(beta))

        return '.'.join(parts)

    @classmethod
    def _get_new_version(cls, current_version, change, is_beta):
        """
        gets a new version based on given current version.

        :param tuple current_version: current version.
        :type current_version: tuple(int major, int minor, int patch, str beta)

        :param str change: change for generating the new version.
        :note change:
            MAJOR = 'major'
            MINOR = 'minor'
            PATCH = 'patch'

        :param bool is_beta: the new version should be a beta one.

        :returns: tuple(int major, int minor, int patch, str beta).
        :rtype: tuple
        """

        major, minor, patch, beta = current_version
        fail_message = 'Change type [{change}] is unknown. ' \
                       'change type must be major or minor or patch.' \
                       .format(change=change)

        if not isinstance(change, str):
            print(fail_message)
            raise Exception(fail_message)

        if change.lower() == 'major':
            major = major + 1
            minor = 0
            patch = 0
        elif change.lower() == 'minor':
            minor = minor + 1
            patch = 0
        elif change.lower() == 'patch':
            patch = patch + 1
        else:
            print(fail_message)
            raise Exception(fail_message)

        beta = None
        if is_beta is True:
            beta = 'beta'

        return major, minor, patch, beta

    @classmethod
    def _upgrade_version(cls, change, is_beta):
        """
        upgrades pyrin version.

        :param str change: change for generating the new version.

        :note change:
            MAJOR = 'major'
            MINOR = 'minor'
            PATCH = 'patch'

        :param bool is_beta: the new version should be a beta one.
        """

        current_version = cls._get_current_version()
        formatted_current_version = cls._format_version(current_version)

        new_version = cls._get_new_version(current_version, change, is_beta)
        formatted_new_version = cls._format_version(new_version)

        print('Current pyrin version is [{current}]'
              .format(current=formatted_current_version))

        cls._set_version(current_version, new_version)

        print('Pyrin version upgraded to [{new}]'
              .format(new=formatted_new_version))

    @classmethod
    def _set_version(cls, old_version, new_version):
        """
        sets the new version in pyrin package.

        :param old_version: old version to be replaced in file.
        :type old_version: tuple(int major, int minor, int patch, str beta)

        :param new_version: new version to be set in file.
        :type new_version: tuple(int major, int minor, int patch, str beta)
        """

        formatted_old = cls._format_version(old_version)
        formatted_new = cls._format_version(new_version)

        with open(cls.PYRIN_VERSION_FILE, 'r') as file:
            file_data = file.read()

        file_data = file_data.replace(formatted_old, formatted_new)

        with open(cls.PYRIN_VERSION_FILE, 'w') as file:
            file.write(file_data)

    @classmethod
    def release(cls, change=None, is_beta=None):
        """
        makes a new release and uploads it.

        :param str change: change for generating the new release version.
                           defaults to `cls.DEFAULT_CHANGE` value if not provided.
        :note change:
            MAJOR = 'major'
            MINOR = 'minor'
            PATCH = 'patch'

        :param bool is_beta: the new release version should be a beta one.
                             defaults to `cls.DEFAULT_IS_BETA` value if not provided.
        """

        if change is None:
            change = cls.DEFAULT_CHANGE

        if is_beta is None:
            is_beta = cls.DEFAULT_IS_BETA

        new_version = None
        current_version = None
        try:
            current_version = cls._get_current_version()
            new_version = cls._get_new_version(current_version, change, is_beta)

            cls._upgrade_version(change, is_beta)
            cls._make()
            cls._upload()
        except Exception:
            print('New release failed.')
            if new_version is not None and current_version is not None:
                cls._set_version(new_version, current_version)
        finally:
            try:
                cls._clear()
            except Exception:
                print('Could not clear release files.')

    @classmethod
    def _make(cls):
        """
        makes release files.
        """

        cls._execute_command('cd ../.. ; python3.7 setup.py sdist bdist_wheel')

    @classmethod
    def _upload(cls):
        """
        uploads the release files to pypi.
        """

        cls._execute_command('cd ../.. ; python3.7 -m twine upload dist/*')

    @classmethod
    def _clear(cls):
        """
        clears released files.
        """

        cls._execute_command('cd ../.. ; rm -r build/ dist/ ; cd src ; rm -r pyrin.egg-info/')

    @classmethod
    def _execute_command(cls, command):
        """
        executes command on shell.

        :param str command: command to be executed.
        """

        subprocess.check_call(command, shell=True)


if __name__ == '__main__':
    fire.Fire(ReleaseManager)
