import mysql.connector
from mysql.connector import Error
import os
from tidb import TiDB
import sys

class DatabaseInitializer:
    def __init__(self, db_name="test", schema_dir="."):
        self.db_name = db_name
        self.schema_dir = schema_dir
        self.db = TiDB()
        self.connection = None
        self.cursor = None

    def read_sql_file(self, file_name):
        file_path = os.path.join(self.schema_dir, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: Schema file '{file_path}' not found.")
        with open(file_path, "r") as file:
            return file.read()

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            print(f"Database '{self.db_name}' created successfully.")
        except Error as e:
            print(f"Error creating database: {e}")

    def create_tables(self, sql_statements):
        try:
            for statement in sql_statements.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)
            print("Tables created successfully.")
        except Error as e:
            print(f"Error creating tables: {e}")

    def drop_database(self):
        try:
            self.cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            print(f"Database '{self.db_name}' dropped if it existed.")
        except Error as e:
            print(f"Error dropping database: {e}")

    def initialize_database(self, sql_file_name):
        sql_statements = self.read_sql_file(sql_file_name)
        self.connection = self.db.get_connection()

        try:
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                self.drop_database()
                self.create_database()
                self.cursor.execute(f"USE {self.db_name}")
                self.create_tables(sql_statements)
                self.connection.commit()
                self.verify_tables()

        except Error as e:
            print(f"Error: {e}")
        finally:
            self.close_connection()

    def verify_tables(self):
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")

def main():
    initializer = DatabaseInitializer()
    initializer.initialize_database(sys.argv[1])
    # initializer.initialize_database("init_db.sql")

if __name__ == "__main__":
    main()
