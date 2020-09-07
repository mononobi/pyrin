# -*- coding: utf-8 -*-
"""
caching globals module.
"""

# this value must be passed to caches when
# no count limit is required.
NO_LIMIT = 'No Limit'

# these are common types that are not hashable and require conversion.
# note that despite tuple is hashable itself, but we have to validate all
# of its internal values to be also hashable. so we have to put tuple in this list.
NOT_HASHABLE_TYPES = (list, dict, set, tuple)
