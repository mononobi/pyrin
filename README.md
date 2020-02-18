# Pyrin

A rich application framework to build apps using Flask on top of it.

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

# Installing

**Install using pip**:

**`pip install pyrin`**

# Running Tests

To be able to run tests, you must notice that:

1. Pyrin tests are developed using pytest, you should first 
   install pyrin tests dependencies using pip:
   
   **`pip install pyrin[tests]`**
 
2. You should create a `.env` file inside `src` directory containing all the configuration 
   keys that have null value in their corresponding settings file. A sample `.env`
   file is available in `samples` that could be used for testing.

3. An entry with `pyrin.server` value should also be created in `/etc/hosts` file.

4. Now you could execute `src/start_tests.py` to start all tests.

# Contribute In Pyrin Development

You must execute `scripts/setup/install-dependencies.sh` first.
Then open the project in your IDE and create required pipenv environment.
Then you could start developing Pyrin.

# Demo Application

A demo application developed using pyrin is available at:
[pyrin-sample](https://github.com/mononobi/pyrin-sample)


# Absolute Simple Usage Example

To be able to create an application based on pyrin, the only thing that is required to do
is to subclass from pyrin `Application` class in your application package. this is 
needed for Pyrin to be able to find out your application path for generating different 
paths and also loading your application packages. there is no difference where to put 
your subclassed `Application`, in this example we put it inside the project's main 
package, inside `__init__.py`


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
from sqlalchemy import Unicode, SmallInteger

from pyrin.database.orm.types.custom import GUID
from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn


class GuestEntity(CoreEntity):

    __tablename__ = 'guest'

    id = CoreColumn(name='id', type_=GUID, primary_key=True, exposed=False)
    name = CoreColumn(name='name', type_=Unicode(100))
    age = CoreColumn(name='age', type_=SmallInteger)

    def primary_key(self):
        return self.id
```

**`api.py:`**

```python
import pyrin.globalization.datetime.services as datetime_services

from pyrin.api.router.decorators import api
from pyrin.core.context import DTO
from pyrin.database.services import get_current_store
from pyrin.utils.unique_id import generate_uuid4

from demo.models import GuestEntity


@api('/introduce/<name>', login_required=False)
def introduce(name, **options):
    store = get_current_store()
    id = generate_uuid4()
    guest = GuestEntity(id=id, name=name)
    store.add(guest)
    return 'Hello dear {name}, you have been added to our app.'.format(name=name)


@api('/guests', login_required=False)
def guests(**options):
    store = get_current_store()
    return store.query(GuestEntity).all()


@api('/', login_required=False)
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

Application will be available at **`127.0.0.1:9081`** by default.

Pyrin on default configurations, will use an **`in-memory sqlite`** database.
