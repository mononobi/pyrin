# -*- coding: utf-8 -*-
"""
utils custom_print module.
"""

import colorama

import pyrin.application.services as application_services


def print_colorful(value, color, force=False):
    """
    prints the given value into stdout using the given color.
    if the application has been started in scripting mode
    it does not print the value.

    :param object value: value to be printed.

    :param int color: color of text to be printed.
                      it should be from `colorama.Fore` colors.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    if force is True or application_services.is_scripting_mode() is False:
        try:
            if not isinstance(value, str):
                value = str(value)
            colorama.init(autoreset=True)
            print(str(color) + value)
        finally:
            colorama.deinit()


def print_warning(value, force=False):
    """
    prints the given value into stdout as a warning.
    if the application has been started in scripting mode
    it does not print the value.

    :param object value: value to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(value, colorama.Fore.YELLOW, force)


def print_error(value, force=False):
    """
    prints the given value into stdout as an error.
    if the application has been started in scripting mode
    it does not print the value.

    :param object value: value to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(value, colorama.Fore.RED, force)


def print_info(value, force=False):
    """
    prints the given value into stdout as an info.
    if the application has been started in scripting mode
    it does not print the value.

    :param object value: value to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(value, colorama.Fore.BLUE, force)


def print_default(value, force=False):
    """
    prints the given value into stdout with default color.
    if the application has been started in scripting mode
    it does not print the value.

    :param object value: value to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(value, colorama.Fore.RESET, force)
