# -*- coding: utf-8 -*-
"""
core compat module.
"""

from test import support


# as OrderedDict implementation is in C, we cannot subclass it normally. so
# we have to forcefully use the python implementation when we want to subclass it.
# this is mainly used in caching container and cacheable dict implementations.
py_module = support.import_fresh_module('collections', blocked=['_collections'])
PythonOrderedDict = py_module.OrderedDict
