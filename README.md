# Pyrin

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

# Installing

install using pip:

pip install pyrin

# Running Tests

to be able to run tests, it is required to:

1. tests are developed using pytest, you should first 
   install pyrin tests dependencies using pip:
   
   pip install pyrin[tests]
 
2. create a '.env' file inside 'src' directory containing all the configuration 
   keys that have null value in their corresponding settings file. a sample '.env'
   file is available in 'samples/dotenv' that could be used for testing.

3. an entry with 'pyrin.server' value should also be created in '/etc/hosts' file.

4. execute 'src/start_test.py' script to start all tests.

# Contribute In Pyrin Development

first you must execute 'scripts/setup/install-dependencies.sh' script.
then open the project in your IDE and create required pipenv environment.
then you could start developing pyrin.

# Demo Application

a demo application developed using pyrin is available at:
https://github.com/mononobi/pyrin-sample
