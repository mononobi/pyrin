# pyrin

a core application to build apps using flask on top of it.

this is neither a framework nor any kind of fork from flask. this is just a rich layer built on top of flask micro-framework to make life easier for developers who want to develop an enterprise application using flask, without having to make their own core layer and getting better code design and structure that is more maintainable.

pyrin could be used as the main package of an application, so other application packages will use it's functionality and features to maintain their goals without worrying about basic implementations.

pyrin point of view is to build an application that is more decoupled, so making it possible to have customized implementations of different packages and also making it easier to write unit-test packages.

another major fact of pyrin is to avoid centralized locations for application features, so a team of multiple developers be able to work on the same repository without facing conflicts here and there. and also reducing the chances of annoying bugs due to forgetting to register something in somewhere.
