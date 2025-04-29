import sqlite3
from sqlite3 import Error
import sys
import os
from DBController import DBController

db_controller = None

#Clears the terminal
def clear_term():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# asks the user to connect to a datbase and if it does not exist then if they want to create it
def userConnection():
    global db_controller 

    db_name = input("Enter database name: ")
    db_exists = os.path.exists(db_name)

    if not db_exists:
        clear_term()
        print(f"The database {db_name} does not exist. \n")
        res = input("Do you want to create it with predetermined data? (Y/N): ")
    
        if res == "N" or res == "n":
            print("Program Exited")
            return
        if res == "Y" or res == "y":
            clear_term()
            db_controller = DBController(db_name)
            print(f"The database {db_name} has been created.")

    else:
        db_controller = DBController(db_name)


# starting method that clears the terminal and initiates the first connection method
def main():
    print("main")
    clear_term()
    userConnection()

if __name__ == "__main__":
    main()