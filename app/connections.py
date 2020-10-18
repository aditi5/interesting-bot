import os
import sys

import psycopg2
from psycopg2.extras import execute_values, DictCursor

from app.settings import TABLE_NAME, TABLE_COLUMNS
from logging import getLogger

logger = getLogger(__name__)


class Connections:
    """
    Connections service class
    """
    __conn = None

    def __init__(self):
        if Connections.__conn is not None:
            raise Exception("This class is a singleton!")
        else:
            # creating database connection.
            conn = self._db_connection()
            Connections.__conn = conn

    @staticmethod
    def get_instance():
        """
        Constructor to initialize Db connection.
        """
        if Connections.__conn is None:
            Connections()
        return Connections.__conn

    def _db_connection(self):
        """
        :return: Receives credentials from environmen variables
                and returns a database connection
        """
        db_config = {
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT'))
        }
        try:
            # connecting to database server
            connection = psycopg2.connect(**db_config)
            logger.info("Connected successfully to PostgreSQL Server.")
        except Exception as error:
            logger.error("ERROR: Unable to connect to PostgreSQL Server. - {}".format(error))
            sys.exit()

        return connection


class DBOps:
    """
    DB service class act as layer between DB and views.
    """

    def __init__(self):
        self.conn = Connections.get_instance()
        self.cur = self.conn.cursor()

    def add_record(self, add_record, table=TABLE_NAME):
        """
        Function to add a record into db.
        """

        if not add_record:
            return

        insert_query = "INSERT INTO {}{} VALUES %s".format(
            table, TABLE_COLUMNS)
        try:
            execute_values(self.cur, insert_query, [add_record])
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def search_query(self, query, table=TABLE_NAME, limit=3):
        """
        Returns list of record dictionaries.
        """
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute(
            "SELECT result, created_by FROM {} WHERE result like '%{}%' order by created_at DESC LIMIT {};".format(
                table, query, limit))
        result = cursor.fetchall()
        cursor.close()
        return result
