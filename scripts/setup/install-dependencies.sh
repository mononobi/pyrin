#!/bin/sh

force_update="n"
# shellcheck disable=SC2039
read -r -p "Force update all installed dependencies? [y/N] " force_update

force_update_length=${#force_update}
if [ "$force_update_length" = "0" ]
then
    force_update="n"
fi

# installing gcc.
gcc_path=$(command -v gcc)
gcc_length=${#gcc_path}

if [ "$gcc_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing gcc."
    apt-get install gcc
else
    echo "gcc is already installed."
fi

# installing syslog.
syslog_path=$(command -v syslog-ng)
syslog_length=${#syslog_path}

if [ "$syslog_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing syslog."
    apt-get install syslog-ng-core
else
    echo "syslog is already installed."
fi

# installing python2.7
python27_path=$(command -v python2.7)
python27_length=${#python27_path}

if [ "$python27_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing python2.7 and dependencies."
    apt-get install python2.7
    apt install python-pip
else
    echo "python2.7 is already installed."
fi

# installing python3.7
python_path=$(command -v python3.7)
python_length=${#python_path}

if [ "$python_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing python3.7 and dependencies."
    apt update
    apt install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa
    apt install python3.7
    apt-get install python3-pip
else
    echo "python3.7 is already installed."
fi

# installing pipenv.
pipenv_path=$(command -v pipenv)
pipenv_length=${#pipenv_path}

if [ "$pipenv_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing pipenv."
    pip install pipenv
else
    echo "pipenv is already installed."
fi
