## Development Instructions

1. Clone the repository:
    ```sh
    $ https://github.com/QueGroup/que-account.git
    ```

2. Create a `.env` file in the root directory of the project and copy the contents of the `.env.template` file into it.

The .env file contains environment variables required for the application to run. The following table describes each
variable:

| Variable                     | Type | Importance | Description                                                                             |
|------------------------------|------|------------|-----------------------------------------------------------------------------------------|
| APP_HOST                     | str  | True       | Host of our application                                                                 |
| APP_PORT                     | int  | True       | Port of our application                                                                 |
| POSTGRES_USER                | str  | True       | Username of the database owner                                                          |
| POSTGRES_PASSWORD            | str  | True       | Password from the database                                                              |
| POSTGRES_DB                  | str  | True       | Database name                                                                           |
| DB_HOST                      | str  | True       | IP address of the database (Name of the service in the docker-compose.yml (User `db`)). |
| DB_PORT                      | str  | True       | The database port. Usually the db running on port `5432`                                |
| REDIS_HOST                   | str  | True       | Redis host                                                                              |
| REDIS_PORT                   | str  | True       | Redis port                                                                              |
| REDIS_PASSWORD               | str  | False      | Redis password                                                                          |
| SECRET_JWT_KEY               | str  | True       | Secret key for jwt generation                                                           |
| ALGORITHM                    | str  | True       | Algorithm for decode jwt token                                                          |
| ACCESS_TOKEN_COOKIE_SAMESITE | str  | True       | IDK                                                                                     |
| ACCESS_TOKEN_COOKIE_HTTPONLY | bool | True       | Can jwt pair store in cookie and they will be http only                                 |
| ACCESS_TOKEN_SECURE          | bool | True       | IDK                                                                                     |
| SESSION_COOKIE_NAME          | str  | True       | Name of session cookie                                                                  |
| SIGNATURE_SECRET_KEY         | str  | True       | Secret key for decode signature from telegram                                           |
| BOT_TOKEN                    | str  | True       | Bot token for notification user                                                         |

3. Run the following command to start the application:
   ```sh
   $ docker-compose up
   ```

This command will start all the services defined in the docker-compose.yml file

Mkdocs on: http://localhost:15321/
API on: http://127.0.0.1:8080/
Grafana on: http://localhost:3000/