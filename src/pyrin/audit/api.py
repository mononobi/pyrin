# -*- coding: utf-8 -*-
"""
audit api module.
"""

import pyrin.audit.services as audit_services

from pyrin.api.router.decorators import api


audit_config = audit_services.get_audit_configurations()
audit_config.update(no_cache=True)
is_enabled = audit_config.pop('enabled', False)

if is_enabled is True:
    @api(**audit_config)
    def inspect(**options):
        """
        inspects all registered packages and gets inspection data.
        ---
        parameters:
          - name: application
            type: boolean
            description: specifies that application info must be included
          - name: packages
            type: boolean
            description: specifies that loaded packages info must be included
          - name: framework
            type: boolean
            description: specifies that framework info must be included
          - name: python
            type: boolean
            description: specifies that python info must be included
          - name: os
            type: boolean
            description: specifies that operating system info must be included
          - name: hardware
            type: boolean
            description: specifies that hardware info must be included
          - name: database
            type: boolean
            description: specifies that database info must be included
          - name: caching
            type: boolean
            description: specifies that caching info must be included
          - name: celery
            type: boolean
            description: specifies that celery info must be included
          - name: traceback
            type: boolean
            description: specifies that on failure, it must include the traceback of errors
        responses:
          200:
            description: all packages are working normally
            schema:
              properties:
                application:
                  type: object
                  description: application info
                packages:
                  type: object
                  description: loaded packages info
                framework:
                  type: object
                  description: framework info
                python:
                  type: object
                  description: python info
                platform:
                  type: object
                  description: platform info
                database:
                  type: object
                  description: database info
                caching:
                  type: object
                  description: caching info
                celery:
                  type: object
                  description: celery info
          500:
            description: some packages have errors
            schema:
              properties:
                application:
                  type: object
                  description: application info
                packages:
                  type: object
                  description: loaded packages info
                framework:
                  type: object
                  description: framework info
                python:
                  type: object
                  description: python info
                platform:
                  type: object
                  description: platform info
                database:
                  type: object
                  description: database info
                caching:
                  type: object
                  description: caching info
                celery:
                  type: object
                  description: celery info
        """

        return audit_services.inspect(**options)
