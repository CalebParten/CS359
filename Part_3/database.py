import sqlite3
from sqlite3 import Error
import sys

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("[INFO] Connection established: " + sqlite3.sqlite_version)

    except Error as e:
        print(e)

    return conn

def close_connection(conn):
    conn.close()

def create_database(conn):
    raw_crtdb = open("crtdb.sql","r")
    script_crtdb = raw_crtdb.read()

    try:
        curs = conn.cursor()
        curs.executescript(script_crtdb)
        print("Tables Created")
    except Error as e:
        print(e)
    return

def insert_data(conn):
    raw_insdb = open("insdb.sql")
    script_insdb = raw_insdb.read()

    try:
        curs = conn.cursor()
        curs.executescript(script_insdb)
        print("Data Inserted into Tables")
    except Error as e:
        print(e)

def query_selection(number):
    if(number == 1):
        print("doing query 1")
    elif(number == 2):
        print("doing query 2")
    elif(number == 3):
        print("doing query 3")
    elif(number == 4):
        print("doing query 4")
    elif (number == 5):
        print("doing query 5")
    elif (number == 6):
        print("doing query 6")
    elif (number == 7):
        print("doing query 7")
    elif (number == 8):
        print("doing query 8")
    elif (number == 9):
        print("doing query 9")
    elif (number == 10):
        print("doing query 10")
    else:
        print("error: argument was not valid")
    
def main():
    conn = create_connection("xyz.sqlite")
    # create_database(conn)
    # insert_data(conn)
    command_num = sys.argv[1]
    i = 0
    while (i < 12):
        query_selection(i)
        i += 1
    # query_selection(int(command_num))



if __name__ == "__main__":
    main()
