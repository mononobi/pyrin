# -*- coding: utf-8 -*-
"""
database handlers module.
"""

import pyrin.database.services as database_services
import pyrin.application.services as application_services

application_services.register_after_request_handler(database_services.finalize_transaction)
application_services.register_teardown_request_handler(database_services.cleanup_session)
