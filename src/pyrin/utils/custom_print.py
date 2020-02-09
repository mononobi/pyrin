# -*- coding: utf-8 -*-
"""
utils custom_print module.
"""

import colorama

import pyrin.application.services as application_services


def print_colorful(text, color, force=False):
    """
    prints the given text into stdout using the given color.
    if the application has been started in scripting mode
    it does not print the text.

    :param str text: text to be printed.

    :param int color: color of text to be printed.
                      it should be from `colorama.Fore` colors.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    if force is True or application_services.is_scripting_mode() is False:
        try:
            colorama.init(autoreset=True)
            print(str(color) + text)
        finally:
            colorama.deinit()


def print_warning(text, force=False):
    """
    prints the given text into stdout as a warning.
    if the application has been started in scripting mode
    it does not print the text.

    :param str text: text to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(text, colorama.Fore.YELLOW, force)


def print_error(text, force=False):
    """
    prints the given text into stdout as an error.
    if the application has been started in scripting mode
    it does not print the text.

    :param str text: text to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(text, colorama.Fore.RED, force)


def print_info(text, force=False):
    """
    prints the given text into stdout as an info.
    if the application has been started in scripting mode
    it does not print the text.

    :param str text: text to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(text, colorama.Fore.BLUE, force)


def print_default(text, force=False):
    """
    prints the given text into stdout with default color.
    if the application has been started in scripting mode
    it does not print the text.

    :param str text: text to be printed.

    :param bool force: forces the printing, even if application
                       has been started in scripting mode.
                       defaults to False if not provided.
    """

    print_colorful(text, colorama.Fore.RESET, force)
