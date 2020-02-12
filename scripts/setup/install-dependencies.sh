#!/bin/bash

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

# installing g++.
gpp_path=$(command -v g++)
gpp_length=${#gpp_path}

if [ "$gpp_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing g++."
    apt-get install g++
else
    echo "g++ is already installed."
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
    echo "Installing python2.7"
    apt-get install python2.7
else
    echo "python2.7 is already installed."
fi

# installing pip.
pip_path=$(command -v pip)
pip_length=${#pip_path}

if [ "$pip_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing pip."
    apt-get install python-pip
else
    echo "pip is already installed."
fi

# installing python3.7
python37_path=$(command -v python3.7)
python37_length=${#python37_path}

if [ "$python37_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing python3.7"
    apt update
    apt install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa
    apt install python3.7
else
    echo "python3.7 is already installed."
fi

# installing pip3
pip3_path=$(command -v pip3)
pip3_length=${#pip3_path}

if [ "$pip3_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing pip3"
    apt update
    apt install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa
    apt-get install python3-pip
else
    echo "pip3 is already installed."
fi

# installing pipenv.
pipenv_path=$(command -v pipenv)
pipenv_length=${#pipenv_path}

if [ "$pipenv_length" = "0" ] || [ $force_update = "Y" ] || [ $force_update = "y" ]
then
    echo "Installing pipenv."
    python3.7 -m pip install pipenv
    pip install pipenv
    pip3 install pipenv
else
    echo "pipenv is already installed."
fi

# installing google fire.
echo "Installing google fire."
python3.7 -m pip install fire
pip install fire
pip3 install fire
