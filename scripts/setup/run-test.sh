#!/bin/sh

cd /var/app_root/pyrin_framework/app/ || exit 1
pipenv run python ./start_test.py
