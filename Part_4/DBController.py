import sqlite3
from sqlite3 import Error
import sys
import os

class DBController:

    # constructor that will create a controller
    def __init__(self, database_name):
        self.conn = None
        self.db_name = database_name
        db_exists = os.path.exists(self.db_name)
        self.create_connection(self.db_name)

        if not db_exists:
            self.create_database()
            self.insert_data()
        
        self.close_connection()
        
    #creates a connection to the database with the supplied name
    def create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            print("[INFO] Connection established: " + sqlite3.sqlite_version)

        except Error as e:
            print(e)

        self.conn = conn

    # uses the crtdb.sql file to create tables
    def create_database(self):
        raw_crtdb = open("crtdb.sql","r")
        script_crtdb = raw_crtdb.read()

        try:
            curs = self.conn.cursor()
            curs.executescript(script_crtdb)
            print("Tables Created")
        except Error as e:
            print(e)
        return
    
    # inserts data according to insdb.sql
    def insert_data(self):
        raw_insdb = open("insdb.sql")
        script_insdb = raw_insdb.read()

        try:
            curs = self.conn.cursor()
            curs.executescript(script_insdb)
            print("Data Inserted into Tables")
        except Error as e:
            print(e)
    
    # closes the connection to the database
    def close_connection(self):
        self.conn.close()
        print("[INFO] Connection Terminated: " + sqlite3.sqlite_version)

    def getName(self):
        return self.db_name
