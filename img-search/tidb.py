import mysql.connector
import os
import sys


"""TiDB connection class"""
PASS = os.getenv("TIDB_PASS")


class TiDB:
    """Do basic CRUD operations."""

    def __init__(
        self, password: str = PASS, database: str = "", autocommit: bool = True
    ):
        try:
            self.connection = mysql.connector.connect(
                host="gateway01.us-east-1.prod.aws.tidbcloud.com",
                port=4000,
                user="2s5azfALGtC83jk.root",
                password=password,
                autocommit=autocommit,
                # connection_timeout=3000,
            )
            self.database = ""
            if database:
                self.connection.database = database
                self.database = database
        except mysql.connector.Error as err:
            raise ValueError(f"Something went wrong connecting to database: {err}")

    def get_connection(self):
        return self.connection

    def close(self):
        self.connection.close()

    def use(self, database_name:str=""):
        """Without an argument, return name of current database. With argument, use it."""
        if database_name:
            try:
                self.connection.database = database_name
                self.database = database_name
            except mysql.connector.Error as err:
                raise ValueError(f"Something went wrong switching to database {database_name}: {err}")
        return self.database

    def query_execute(self, query):
        try:
            with self.connection.cursor() as cur:
                return cur.execute(query)
        except mysql.connector.Error as err:
            raise ValueError(f"Error executing query: {err}\nQuery:\n{query}")

    def query(self, query):
        try:
            with self.connection.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
            return result
        except mysql.connector.Error as err:
            raise ValueError(f"Error executing query: {err}\nQuery:\n{query}")

    def query_rollback(self, query, params=None):
        try:
            with self.connection.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                result = cur.fetchall()
            self.connection.commit()  # Commit changes for non-SELECT queries
            return result
        except mysql.connector.Error as err:
            self.connection.rollback()  # Rollback in case of error
            raise ValueError(f"Error executing query: {err}\nQuery:\n{query}")
        
    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
