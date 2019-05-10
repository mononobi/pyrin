# -*- coding: utf-8 -*-
"""
utils custom_print module.
"""

from colorama import init, deinit, Fore


def print_colorful(text, color):
    """
    prints the given text into stdout using the given color.

    :param str text: text to be printed.

    :param int color: color of text to be printed.
                      it should be from `colorama.Fore` colors.
    """

    try:
        init(autoreset=True)
        print(str(color) + text)
    finally:
        deinit()


def print_warning(text):
    """
    prints the given text into stdout as a warning.

    :param str text: text to be printed.
    """

    print_colorful(text, Fore.YELLOW)


def print_error(text):
    """
    prints the given text into stdout as an error.

    :param str text: text to be printed.
    """

    print_colorful(text, Fore.RED)


def print_info(text):
    """
    prints the given text into stdout as an info.

    :param str text: text to be printed.
    """

    print_colorful(text, Fore.BLUE)
