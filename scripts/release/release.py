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

    def _get_current_version(self):
        """
        gets current pyrin version from pyrin package.

        :returns: tuple(int major, int minor, int patch, str beta)
        :rtype: tuple
        """

        with io.open(self.PYRIN_VERSION_FILE, 'rt', encoding='utf8') as version_file:
            version = re.search(r"__version__ = '(.*?)'", version_file.read()).group(1)

        parts = version.split('.')
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])

        beta = None
        if len(parts) > 3:
            beta = parts[3]

        return major, minor, patch, beta

    def _format_version(self, version):
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

    def _get_new_version(self, current_version, change, is_beta):
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

        :returns: tuple(int major, int minor, int patch, str beta)
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

        return self._normalize_version(major, minor, patch, beta)

    def _normalize_version(self, major, minor, patch, beta):
        """
        normalizes given version to be under correct range.
        maximum minor and patch number is 30, if they go upper
        than that, the previous version part will be increased by 1,
        and the value itself will be set to zero.
        for example if the current version number is `1.30.29` and we
        generate a new 'minor' version, the new version will be `1.31.0`.
        then the normalize function will change it into `2.0.0`.

        :param int major: major version number.
        :param int minor: minor version number.
        :param int patch: patch version number.
        :param str beta: beta version flag.

        :returns: tuple(int major, int minor, int patch, str beta)
        :rtype: tuple
        """

        if patch > 30:
            minor = minor + 1
            patch = 0

        if minor > 30:
            major = major + 1
            minor = 0
            patch = 0

        return major, minor, patch, beta

    def _upgrade_version(self, change, is_beta):
        """
        upgrades pyrin version.

        :param str change: change for generating the new version.

        :note change:
            MAJOR = 'major'
            MINOR = 'minor'
            PATCH = 'patch'

        :param bool is_beta: the new version should be a beta one.
        """

        current_version = self._get_current_version()
        formatted_current_version = self._format_version(current_version)

        new_version = self._get_new_version(current_version, change, is_beta)
        formatted_new_version = self._format_version(new_version)

        print('Current pyrin version is [{current}]'
              .format(current=formatted_current_version))

        self._set_version(current_version, new_version)

        print('Pyrin version upgraded to [{new}]'
              .format(new=formatted_new_version))

    def _set_version(self, old_version, new_version):
        """
        sets the new version in pyrin package.

        :param old_version: old version to be replaced in file.
        :type old_version: tuple(int major, int minor, int patch, str beta)

        :param new_version: new version to be set in file.
        :type new_version: tuple(int major, int minor, int patch, str beta)
        """

        formatted_old = self._format_version(old_version)
        formatted_new = self._format_version(new_version)

        with open(self.PYRIN_VERSION_FILE, 'r') as file:
            file_data = file.read()

        file_data = file_data.replace(formatted_old, formatted_new)

        with open(self.PYRIN_VERSION_FILE, 'w') as file:
            file.write(file_data)

    def release(self, change=None, is_beta=None):
        """
        makes a new release and uploads it.

        :param str change: change for generating the new release version.
                           defaults to `DEFAULT_CHANGE` value if not provided.
        :note change:
            MAJOR = 'major'
            MINOR = 'minor'
            PATCH = 'patch'

        :param bool is_beta: the new release version should be a beta one.
                             defaults to `DEFAULT_IS_BETA` value if not provided.
        """

        if change is None:
            change = self.DEFAULT_CHANGE

        if is_beta is None:
            is_beta = self.DEFAULT_IS_BETA

        new_version = None
        current_version = None
        try:
            current_version = self._get_current_version()
            new_version = self._get_new_version(current_version, change, is_beta)

            self._upgrade_version(change, is_beta)
            self._make()
            self._upload()
        except Exception:
            print('New release failed.')
            if new_version is not None and current_version is not None:
                self._set_version(new_version, current_version)
        finally:
            try:
                self._clear()
            except Exception:
                print('Could not clear release files.')

    def _make(self):
        """
        makes release files.
        """

        self._execute_command('cd ../.. ; python3.7 setup.py sdist bdist_wheel')

    def _upload(self):
        """
        uploads the release files to pypi.
        """

        self._execute_command('cd ../.. ; python3.7 -m twine upload dist/*')

    def _clear(self):
        """
        clears released files.
        """

        self._execute_command('cd ../.. ; rm -r build/ dist/ ; cd src ; rm -r pyrin.egg-info/')

    def _execute_command(self, command):
        """
        executes command on shell.

        :param str command: command to be executed.
        """

        subprocess.check_call(command, shell=True)


if __name__ == '__main__':
    fire.Fire(ReleaseManager)
