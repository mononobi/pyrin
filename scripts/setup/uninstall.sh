#!/bin/bash

remove="n"
# shellcheck disable=SC2039
read -r -p "Uninstall 'pyrin' application? [y/N] " remove

if [ "$remove" = "Y" ] || [ "$remove" = "y" ]
then
    if [ -d "/var/log/pyrin" ]
    then
        rm -r /var/log/pyrin/*
    fi

    if [ -d "/var/app_root/pyrin_framework" ]
    then
        rm -r /var/app_root/pyrin_framework/
    fi

  echo
  echo -e "\e[0;32m** Uninstallation completed **\e[0m"
  echo
fi
