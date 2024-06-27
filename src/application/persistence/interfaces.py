import abc
from typing import (
    Any,
)

from sqlalchemy import (
    Delete,
    Select,
    Update,
)

from src.shared import (
    UpdateSchemaT,
)


class IRetrieveQuery:
    """
    An interface providing a method for retrieving a query for fetching data.
    """

    @abc.abstractmethod
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        # noinspection PyUnresolvedReferences
        """
        Return a SELECT query for retrieving a single row from the database.

        >>> return select(self.model).filter(*args).filter_by(**kwargs)

        :param args: Filter arguments to be passed to the SELECT query
        :param kwargs: Filter keyword arguments to be passed to the SELECT query
        :return: A SELECT query for retrieving a single row from the database
        """
        raise NotImplementedError()


class IListQuery:
    """
    An interface providing a method for retrieving a query for fetching a list of data.
    """

    @abc.abstractmethod
    def _get_all_query(
            self,
            skip: int = 0,
            limit: int = 10,
            *args: Any,
            **kwargs: Any,
    ) -> Select[tuple[Any]]:
        # noinspection PyUnresolvedReferences
        """
        Return a SELECT query for retrieving multiple rows from the database.

        >>> return select(self.model).offset(skip).limit(limit).filter(*args).filter_by(**kwargs)

        :param skip: The number of rows to skip (optional, default 0)
        :param limit: The maximum number of rows to retrieve (optional, default 10)
        :param args: Filter arguments to be passed to the SELECT query
        :param kwargs: Filter keyword arguments to be passed to the SELECT query
        :return: A SELECT query for retrieving multiple rows from the database
        """
        raise NotImplementedError()


class IUpdateQuery:
    """
    An interface providing a method for retrieving a query for updating data.
    """

    @abc.abstractmethod
    def _update_query(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        # noinspection PyUnresolvedReferences
        """
        Return an UPDATE query for updating a single row in the database.

        >>> return (
        ...     update(self.model)
        ...     .where(self.model.id == pk)
        ...     .values(**data_in.model_dump(exclude_unset=True))
        ...     .filter_by(**kwargs)
        ...     .returning(self.model)
        ...    )

        :param pk: The primary key of the row to be updated
        :param data_in: The updated data to be passed to the UPDATE query
        :param kwargs: Additional keyword arguments to be passed to the UPDATE query
        :return: An UPDATE query for updating a single row in the database
        """
        raise NotImplementedError()


class IDeleteQuery:
    """
    An interface providing a method for retrieving a query for deleting data.
    """

    @abc.abstractmethod
    def _delete_query(self, *args: Any, **kwargs: Any) -> Delete:
        # noinspection PyUnresolvedReferences
        """
        Return a DELETE query for deleting one or more rows from the database.

        >>> return Delete(self.model).filter(*args)

        :param args: Filter arguments to be passed to the DELETE query
        :param kwargs: Filter keyword arguments to be passed to the DELETE query
        :return: A DELETE query for deleting one or more rows from the database
        """
        raise NotImplementedError()


class IRLUDQuery(
    abc.ABC,
    IRetrieveQuery,
    IListQuery,
    IUpdateQuery,
    IDeleteQuery,
):
    """
    An interface providing methods for retrieving, updating, and deleting data.
    """
    pass
