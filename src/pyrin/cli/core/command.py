# -*- coding: utf-8 -*-
"""
cli core cli module.
"""

import os
import sys


python_path = os.path.abspath('../../..')
os.environ['PYTHONPATH'] = python_path
sys.path.append(python_path)


import pyrin.cli.core.services as core_services

from pyrin.utils.custom_print import print_error


if __name__ == '__main__':
    try:
        handler_name = sys.argv[1]
        core_services.create(handler_name)
    except IndexError:
        print_error('Please input the command name.', force=True)
    except Exception as error:
        print_error(error, force=True)
