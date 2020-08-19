# -*- coding: utf-8 -*-
"""
database handlers module.
"""

import pyrin.application.services as application_services
import pyrin.database.services as database_services


application_services.register_teardown_request_handler(database_services.cleanup_session)
