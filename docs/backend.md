## About of the structure

**Structure**:

```
src/
├── application
│ ├── dto
│ ├── mixins
│ ├── service
│ └── strategies.py
├── domain
│ ├── auth
│ ├── common
│ └── user
├── infrastructure
│ ├── database
│ │ ├── models
│ │ ├── redis.py
│ │ └── repositories
│ ├── log
│ ├── services
│ │ └── security
│ └── settings.py
├── main.py
├── presentation
│ └── api
│     ├── controllers
│     ├── exceptions.py
│     ├── middlewares
│     └── providers
└── shared
```

---

### Detailed description

#### `application/`

This is the core of application, where the business logic resides. It contains the following
subdirectories:

- `dto/`: Data Transfer Objects are used to transfer data between processes or between tiers in a layered architecture.
- `mixins/`: Contains several mixin classes that provide methods for interacting with a database using SQLAlchemy.
- `queries/`: Contains classes that are responsible for generating queries to the database.
- `service/`: Contains classes that implement the business logic of the application. These classes use the repositories
  to interact with the database.
- `strategies.py`: Contains classes that implement various strategies for working with authentication.

#### `domain/`

The domain module in our application represents the core business logic and entities of the system.

#### `infrastructure/`

The infrastructure module in our application is responsible for providing the technical details and implementation of
the system's core functionalities. It contains the following subdirectories:

- `database/`: This directory contains all the database-related code and
  database repositories. The models subdirectory contains the SQLAlchemy models that represent the tables in the
  database.
- `log/`: This directory contains the logging configuration and setup for the application.
- `services/`: This directory contains the implementation of various services used by the application, such as security
  services.
- `settings.py`: This file contains the configuration settings for the application, such as database connection strings,
  logging configuration, and security settings.

#### `presentation/`

The presentation module in our application is responsible for handling user interactions with the
system. It contains the following subdirectories:

- `api/`: This directory contains all the code related to the API endpoints that are exposed to the users of the system.
  It includes the following subdirectories:
    - `controllers`: This directory contains the controller classes that handle the incoming API requests and responses.
      Each controller class corresponds to a specific API endpoint and contains the methods that implement the business
      logic for that endpoint.
    - `exceptions.py`: This file contains the custom exceptions that are raised by the API endpoints when errors occur.
    - `middlewares`: This directory contains the middleware classes that are used to process incoming API requests
      before they reach the controller classes. The logging middleware, for example, logs the incoming requests and
      responses.
    - `providers`: This directory contains the classes that provide dependencies to the API endpoints. The
      dependencies.py contains the functions that create the instances of the service classes and database repositories
      that are used by the API endpoints. The di_containers.py file contains the code that configures the dependency
      injection container used by the application.

#### `shared/`

The shared module in our application contains code that is shared across different parts of the system.