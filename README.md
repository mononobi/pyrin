# Pyrin

A rich application framework to build apps using Flask on top of it.

Pyrin is an application framework built on top of Flask micro-framework to make 
life easier for developers who want to develop an enterprise application 
using flask, without having to make their own core layer and getting better code
design and structure that is more maintainable.

Pyrin could be used as the parent package of an application, so other application 
packages will use its functionality and features to maintain their goals without 
worrying about basic implementations.
It is also possible for application packages to extend existing Pyrin packages.

Pyrin point of view is to build an application that is more decoupled, so making it 
possible to have customized implementations of different packages and also making it 
easier to write unit-test packages.

Another major fact of pyrin is to avoid centralized locations for application features, so a team
of multiple developers be able to work on the same repository without facing conflicts here
and there. Also reducing the chances of annoying bugs due to forgetting to register
something in somewhere.

# Installing

Install using pip:

pip install pyrin

# Running Tests

To be able to run tests, you must notice that:

1. Pyrin tests are developed using pytest, you should first 
   install pyrin tests dependencies using pip:
   
   pip install pyrin[tests]
 
2. You should create a '.env' file inside 'src' directory containing all the configuration 
   keys that have null value in their corresponding settings file. A sample '.env'
   file is available in 'samples/dotenv' that could be used for testing.

3. An entry with 'pyrin.server' value should also be created in '/etc/hosts' file.

4. Now you could execute 'src/start_tests.py' script to start all tests.

# Contribute In Pyrin Development

You must execute 'scripts/setup/install-dependencies.sh' script first.
Then open the project in your IDE and create required pipenv environment.
Then you could start developing pyrin.

# Demo Application

A demo application developed using pyrin is available at:
https://github.com/mononobi/pyrin-sample
