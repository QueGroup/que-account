## Database Service

QueAccount's data infrastructure is built on psql, deployed using Docker for easy management and scaling.

---

### Why SQLAlchemy and Alembic?

- **SQLAlchemy**: This is an Object-Relational Mapping (ORM) library for Python. It allows you to interact with
  databases using Python objects, abstracting away much of the SQL. This makes database interactions more intuitive and
  less error-prone.

- **Alembic**: Alembic, designed to work with SQLAlchemy, manages database migrations. As your application grows and
  changes, so too will your database schema. Alembic helps manage these changes, ensuring data integrity.


### Database Diagram: Tables and Relations

Coming soon...

### Working with Data

To interact with the database using the provided mixins and classes, follow these steps:

#### 1. Define Model Class

   Define your SQLAlchemy model classes representing your database tables. These classes should inherit from `Base` and
   should be created in the `src/infrastructure/database/models/` directory.

   ```python
   class SomeModel(Base):
        __tablename__ = "some_models"
        id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True, unique=True)
        # Define other columns as needed
   ```

#### 2. Create a QueryMixin Class

   Create a QueryMixin class for the new model. These classes should inherit from the appropriate query mixin class and
   provide methods for CRUD operations specific to the entity. Create them in the `src/application/mixins/` directory.
   ```python
   class SomeModelQueryMixin(CRUDMixin[models.SomeModel, entity.SomeModel, dto.SomeModelUpdate]):
        def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
            return select(self.model).filter(*args).filter_by(**kwargs)
        # Define other methods as needed
   ```
#### 3. Create a Repository Class

   Create a repository class that inherits from the QueryMixin class. Create these in the
   `src/infrastructure/database/repositories/` directory.
   ```python
   class SomeModelRepository(SomeModelQueryMixin):
        def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
            super().__init__(session=session_factory, model=models.SomeModel)
   ```

#### 4. Create a Service Class

   Create a service class. This class should not inherit from other classes. Create these in the
   `src/application/service/` directory.

   ```python
   class SomeModelService:
        def __init__(self, some_model_repository: SomeModelRepository) -> None:
            self.repository: SomeModelRepository = some_model_repository

        # Define methods for your service class
   ```

#### 5. Configure the DI Container

   We use singleton providers to ensure that certain objects, such as database connectors and Redis clients, are
   instantiated only once per application instance. This helps conserve resources and maintain consistency across the
   application.

   Factory providers are used to dynamically create instances of objects, such as repository and service classes, with
   their dependencies automatically injected. This promotes flexibility and scalability in our architecture.
   Find Container in the `src/presentation/api/providers/di_containers.py`
   ```python
    class Container(containers.DeclarativeContainer):
        some_repository = providers.Factory(
            SomeModelRepository,
            session_factory=db.provided.get_db_session,
        )
        some_service = providers.Factory(
            SomeModelService,
            user_repository=user_repository,
        )
   ```



