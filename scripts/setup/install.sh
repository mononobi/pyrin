#!/bin/sh

# installing dependencies.
./install-dependencies.sh

# getting working directory path.
working_dir=$(pwd)

# user name that application should be accessible to it.
user_name=app_user

# checking that user_name is present, if not, create it.
user_exists=$(id -u $user_name > /dev/null 2>&1; echo $?)

if [ "$user_exists" != "0" ]
then
    # user does not exist, creating it.
    echo "Creating $user_name."
    adduser $user_name
else
    echo "$user_name is already present."
fi

# adding user_name into www-data and sudo groups.
usermod -aG sudo $user_name
usermod -aG www-data $user_name

# making logging directory and log backup.
if [ ! -d "/var/log/backup/pyrin" ]
then
    mkdir -p /var/log/backup/pyrin/
fi

if [ -d "/var/log/pyrin" ]
then
    echo "Archiving and cleaning up previous logs."
    name=$(date "+%Y.%m.%d.%H.%M.%S")
    tar -czf /var/log/backup/pyrin/"pyrin.log.$name.tar.gz" /var/log/pyrin
    rm -r /var/log/pyrin
fi

mkdir -p /var/log/pyrin/

# setting permissions for log directory.
chown -R root:www-data /var/log/pyrin/
chmod -R 770 /var/log/pyrin/

# making application backup directory and file.
if [ ! -d "/var/app_root/backup/pyrin_framework" ]
then
    mkdir -p /var/app_root/backup/pyrin_framework/
fi

if [ -d "/var/app_root/pyrin_framework" ]
then
    echo "Archiving and cleaning up previous installation."
    name=$(date "+%Y.%m.%d.%H.%M.%S")
    tar -czf /var/app_root/backup/pyrin_framework/"pyrin_framework.$name.tar.gz" /var/app_root/pyrin_framework
    rm -r /var/app_root/pyrin_framework
else
    echo "Performing fresh installation."
fi

# making up required directory.
mkdir -p /var/app_root/pyrin_framework/app/
chown -R $user_name /var/app_root/

echo "Copying applications."
# copying tests application.
cp -r ../../src/tests/ /var/app_root/pyrin_framework/app/tests/
cp ../../src/start_test.py /var/app_root/pyrin_framework/app/start_test.py

# copying pyrin application.
cp -r ../../src/pyrin/ /var/app_root/pyrin_framework/app/pyrin/

# copying .env file.
cp ../../src/.env /var/app_root/pyrin_framework/app/.env

# copying pipenv required files.
cp ../../Pipfile.lock /var/app_root/pyrin_framework/Pipfile.lock
cp ../../Pipfile /var/app_root/pyrin_framework/Pipfile

# creating pipenv environment.
cd /var/app_root/pyrin_framework/ || exit 1
export PIPENV_VENV_IN_PROJECT=1
pipenv install --ignore-pipfile

#returning to working directory.
cd "$working_dir" || exit 1

# setting the owner of directory.
chown -R $user_name /var/app_root/

echo
echo "\e[0;32m ** Installation completed ** \e[0m"
echo
