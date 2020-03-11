# -*- coding: utf-8 -*-
"""
cli core command module.
"""

import sys

import pyrin.cli.core.services as core_services

from pyrin.utils.custom_print import print_error


def main():
    try:
        handler_name = sys.argv[1]
        core_services.create(handler_name)
    except IndexError:
        print_error('Please input the command name.', force=True)
    except Exception as error:
        print_error(error, force=True)
