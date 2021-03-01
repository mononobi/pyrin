# Pyrin

A rich platform-independent application framework to build apps using Flask on top of it.

Pyrin is an application framework built on top of Flask micro-framework to make 
life easier for developers who want to develop an enterprise application 
using Flask, without having to make their own core layer and getting better code
design and structure that is more maintainable.

Pyrin could be used as the parent package of an application, so other application 
packages will use its functionality and features to maintain their goals without 
worrying about basic implementations.
It is also possible for application packages to extend existing Pyrin packages.

Pyrin point of view is to build an application that is more decoupled, so making it 
possible to have customized implementations of different packages and also making it 
easier to write unit-test packages.

Another major fact of Pyrin is to avoid centralized locations for application features, so a team
of multiple developers be able to work on the same repository without facing conflicts here
and there. Also reducing the chances of annoying bugs due to forgetting to register
something in somewhere.

## Installing

**Install using pip**:

**`pip install pyrin`**

## Running Tests

To be able to run tests:

1. Pyrin tests are developed using pytest, you should first 
   install pyrin tests dependencies using pip:
   
**`pip install pyrin[tests]`**

2. Now you could execute **`python3 start_unit.py`** to start all unit tests.

## Demo Application

A demo application developed using Pyrin framework is available at: 
[Pyrin-Demo](https://github.com/mononobi/pyrin_demo)

## Contribute In Pyrin Development

We highly appreciate any kind of contributions to Pyrin development.
Fork Pyrin and implement a new feature and make a pull request, we'll let
you know when your work becomes a part of Pyrin.
So, open the project in your IDE and create your pipenv environment.
Then you could start developing Pyrin.

## Thanks To JetBrains
![](./resources/images/jetbrains.png)

We develop pyrin using [JetBrains](https://www.jetbrains.com/?from=pyrin) products with the 
awesome open source license provided by JetBrains.

## Extremely Simple Usage Example

The sample code below, is just a rapid showcase on how to develop using Pyrin. 
for a real world application, it is best fit to use the concept of dependency injection 
and IoC which Pyrin is built upon.

To be able to create an application based on Pyrin, the only thing that is required to do
is to subclass from pyrin **`Application`** class in your application package. this is 
needed for Pyrin to be able to find out your application path for generating different 
paths and also loading your application packages. there is no difference where to put 
your subclassed **`Application`**, in this example we put it inside the project's main 
package, inside **`__init__.py`**.


**Sample Project Structure:**

- root_dir
  - demo
    - `__init__.py`
    - `api.py`
    - `models.py`
  - `start.py`

**`__init__.py:`**

```python
from pyrin.application.base import Application


class DemoApplication(Application):
    pass
```

**`models.py:`**

```python
from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.columns import GUIDPKColumn, StringColumn, SmallIntegerColumn


class GuestEntity(CoreEntity):

    _table = 'guest'

    id = GUIDPKColumn(name='id')
    name = StringColumn(name='name', max_length=100, validated=True)
    age = SmallIntegerColumn(name='age', min_value=1, validated=True)
```

**`api.py:`**

```python
from pyrin.api.router.decorators import api
from pyrin.core.structs import DTO
from pyrin.database.services import get_current_store

from demo.models import GuestEntity


@api('/introduce/<name>', authenticated=False)
def introduce(name, **options):
    store = get_current_store()
    guest = GuestEntity(name=name)
    store.add(guest)
    return 'Hello dear {name}, you have been added into our database.'.format(name=name)


@api('/guests', authenticated=False)
def guests(**options):
    store = get_current_store()
    return store.query(GuestEntity).all()


@api('/', authenticated=False)
def hello(**options):
    store = get_current_store()
    count = store.query(GuestEntity.id).count()
    result = DTO(message='Welcome to our demo application, please introduce yourself.',
                 current_guests=count)
    return result
```

**`start.py:`**

```python
from demo import DemoApplication


if __name__ == '__main__':
    app = DemoApplication()
    app.run(use_reloader=False)
```

Now you could start application by executing this command in your terminal:

**`python3 start.py`**

Application will be available at **`127.0.0.1:5000`** by default.

Pyrin on default configurations, will use an **`in-memory sqlite`** database.

## Creating a New Pyrin Project

Pyrin has a command line tool that can be used to create a new project.
to use the command line interface of Pyrin, install Pyrin and then open a terminal and write:

```shell
pyrin project
```

after hitting enter, a couple of questions will be asked to create your project, answer
questions accordingly, and your project will be created without a hassle.

## Using Project's Extended Command Line Tool

After creating a new project using **`pyrin project`** command, a **`cli.py`** file will 
be generated in the root of your new project directory. there are a couple of command 
groups that can be used to perform different actions. 
execute each command with **`--help`** option to see all available commands of each group.

- **Builtin Commands:**

  - **`python cli.py alembic`**
  - **`python cli.py babel`**
  - **`python cli.py template`**
  - **`python cli.py security`**
    

- **Integration Commands:**
  - **`python cli.py celery`**

## Integrations

Pyrin has builtin integrations for different services. to use each one of integrations inside
your application, you must install dependencies of that integration.

**Celery:**

**`pip install pyrin[celery]`**

To enable celery after installing its dependencies, open **`settings/packaging.ini`** file
and remove **`pyrin.task_queues.celery`** from the **`ignore_packages`** list.

**Sentry:**

**`pip install pyrin[sentry]`**

To enable sentry after installing its dependencies, open **`settings/packaging.ini`** file
and remove **`pyrin.logging.sentry`** from the **`ignore_packages`** list.

**Redis:**

**`pip install pyrin[redis]`**

To enable redis after installing its dependencies, open **`settings/packaging.ini`** file
and remove **`pyrin.caching.remote.handlers.redis`** from the **`ignore_modules`** list.

**Memcached:**

**`pip install pyrin[memcached]`**

To enable memcached after installing its dependencies, open **`settings/packaging.ini`** file
and remove **`pyrin.caching.remote.handlers.memcached`** from the **`ignore_modules`** list.
