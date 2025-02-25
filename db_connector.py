import pymysql
import sqlite3


class DBConnector:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @classmethod
    def _from_connection(cls, connection):
        cursor = connection.cursor()
        return cls(connection, cursor)

    @classmethod
    def connect_mysql(cls, dbconfig: dict):
        connection = pymysql.connect(**dbconfig)
        return cls._from_connection(connection)

    @classmethod
    def connect_sqlite(cls, db_name):
        connection = sqlite3.connect(db_name)
        connection.row_factory = sqlite3.Row # create dict instead of tuple.

        return cls._from_connection(connection)

    def commit(self):
        try:
            self.connection.commit()
        except pymysql.Error as e:
            print(e)
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()