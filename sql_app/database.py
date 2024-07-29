"""Contains DB manager interface and its realizations."""
from typing import Protocol, Any, TypeVar
import asyncio
from sqlalchemy import create_engine, text, Connection, Row
from sqlalchemy.orm import sessionmaker, Session
# pylint: disable=E0401
from settings import settings

T_co = TypeVar('T_co', covariant=True)


class DBManager(Protocol[T_co]):
    """
    Description of common DB Manager interface.

    Attributes:
      engine: (Connection): The database connection engine.
      session_local: (sessionmaker[Session]): A session maker for
       creating database sessions.
    """

    engine: Connection
    session_local: Session

    async def get_data(self) -> T_co:
        """
        Get data from the database.

        :return: T: The data retrieved from the database.
        """

    async def insert_data(self) -> T_co:
        """
        Insert data into the database.

        :return: T: The data inserted into the database.
        """


class KisDBManager:
    """
    KisDBManager class for managing database operations specific to KIS.

    Attributes:
      engine: (Connection): The database connection engine.
      session_local: (sessionmaker[Session]): A session maker for
       creating database sessions.
    """

    engine: Connection = create_engine(settings.kis_db_url, echo=True).connect()
    session_local: Session = sessionmaker(autoflush=False, bind=engine)()

    async def get_data(self,
                       query_string: str = """SELECT * FROM mm.arrived LIMIT 1;"""
                       ) -> Row[Any] | None:
        """
        Retrieve a row of data from the passed table.

        :return: Row[Any] | None: The first row of data from the table
         or None if no data is found.
        """
        query = text(query_string)
        cursor = self.session_local.execute(query)
        result = cursor.fetchone()
        return result

    async def insert_data(self, query_string: str | None) -> None:
        """
        Insert data.

        :param query_string: String of raw query.
        """


o: KisDBManager = KisDBManager()


async def main() -> Row[Any] | None:
    """
    Run main asynchronous function to retrieve and print data
    from the database.
    """
    result = await o.get_data()
    return result


if __name__ == '__main__':
    print(asyncio.run(main()))
