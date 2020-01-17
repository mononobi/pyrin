# pyrin

core application to build apps using flask on top of it.

pyrin is an application framework built on top of flask micro-framework to make 
life easier for developers who want to develop an enterprise application 
using flask, without having to make their own core layer and getting better code
design and structure that is more maintainable.

pyrin could be used as the side core package of an application, so other application 
packages will use it's functionality and features to maintain their goals without 
worrying about basic implementations.

pyrin point of view is to build an application that is more decoupled, so making it possible to
have customized implementations of different packages and also making it easier to write
unit-test packages.

another major fact of pyrin is to avoid centralized locations for application features, so a team
of multiple developers be able to work on the same repository without facing conflicts here
and there. and also reducing the chances of annoying bugs due to forgetting to register
something in somewhere.

# prerequisites

to be able to run tests, it is required to create a .env file inside src directory
containing all the configuration keys that have null value in their corresponding
settings file. a sample .env file is available in samples/dotenv.

an entry with 'pyrin.server' value should also be created in /etc/hosts file.

# code editing in pycharm

first you should execute the scripts/setup/install-dependencies.sh script.
then open the project in pycharm and it will create required pipenv environment.
then you could start developing the application.

# running tests in pycharm

add a new script in pycharm's edit configurations dialog and choose the src/start_test.py
script. then run or debug it.

# installation

to install the application, you must put a valid .env file inside src directory.
then execute the scripts/setup/install.sh script to install pyrin system-wide, then you'll be
able to run tests using /var/app_root/pyrin_framework/app/run-test.sh script.

# uninstallation

to uninstall the application from system, you should execute the scripts/setup/uninstall.sh
script. be aware that uninstallation process will not make any backup of installed version.

# demo application

a demo application developed using pyrin framework is available at:
https://github.com/mononobi/pyrin-sample
