# -*- coding: utf-8 -*-
"""
common utils module.
"""

import os

import pyrin.application.services as application_services


def create_settings_file(name):
    """
    creates a setting file in settings path.

    :param str name: file name.
    """

    settings_path = application_services.get_settings_path()
    file_path = os.path.join(settings_path, name)
    command = 'touch {path}'.format(path=file_path)
    os.system(command)


def delete_settings_file(name):
    """
    deletes the given settings file.

    :param str name: file name.
    """

    settings_path = application_services.get_settings_path()
    file_path = os.path.join(settings_path, name)
    command = 'rm -r {path}'.format(path=file_path)
    os.system(command)
