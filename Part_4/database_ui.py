import sqlite3
from sqlite3 import Error
import sys
import os
from time import sleep
from DBController import DBController
from Member import *

db_controller = None
debug = False

greeting = '''
      ___          _____          ___     
     /__/\        /  /::\        /  /\    
    |  |::\      /  /:/\:\      /  /:/    
    |  |:|:\    /  /:/  \:\    /  /:/     
  __|__|:|\:\  /__/:/ \__\:|  /  /:/  ___ 
 /__/::::| \:\ \  \:\ /  /:/ /__/:/  /  /\\
 \  \:\~~\__\/  \  \:\  /:/  \  \:\ /  /:/
  \  \:\         \  \:\/:/    \  \:\  /:/ 
   \  \:\         \  \::/      \  \:\/:/  
    \  \:\         \__\/        \  \::/   
     \__\/                       \__\/    
'''

#Clears the terminal
def clearTerm():
    if not debug:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

#checks wether a string can be cast to int
def isInputInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

#prints name of database that is connected
def printConnectionTitle():
    print('='*80)
    print(f'Connected to DB: {db_controller.getName()}')
    print('='*80)
    print('\n')

#prints the title of the menu
def printMenuTitle(title):
    print(f'{title} Menu')
    print('-'*80)

# clears and prints options
def printMainMenuOptions():
    clearTerm()
    printConnectionTitle()
    printMenuTitle('Main')
    print("Please select from the below options using the number:")
    print("1. Members Menu")
    print("2. Classes menu")
    print("3. Equipment menu")
    print("4. Logout and Exit")
    print('-'*80)

# clears and prints options
def printMemberMenuOptions():
    clearTerm()
    printConnectionTitle()
    printMenuTitle('Member')
    print("Please select from the below options using the number:")
    print("1. View All Members")               #1
    print("2. Add a New Member")               #2
    print("3. Update Member Information")      #3
    print("4. Delete Member with ID")          #4
    print("0. Return to Main Menu")
    print('-'*80)

# clears and prints options
def printClassMenuOptions():
    clearTerm()
    printConnectionTitle()
    printMenuTitle('Class')
    print("Please select from the below options using the number:")
    print('1. Classes w/ Attendance')          #5
    print('2. Add New Class')                  #6
    print('3. Update Class Information')       #7
    print('4. Delete Class by ID')             #8
    print('5. Find Members in Class by ID')    #9
    print('0. Return to Main Menu')
    print('-'*80)

# clears and prints options
def printEquipmentMenuOptions():
    clearTerm()
    printConnectionTitle()
    printMenuTitle('Equipment')
    print("Please select from the below options using the number:")
    print('1. Show All Equipment')             #10
    print('2. Add New Equipment')              #11
    print('3. Update Equipment Information')   #12
    print('4. Delete Equipment by ID ')        #13
    print('0. Return to Main Menu')
    print('-'*80)

# asks the user to connect to a datbase and if it does not exist then if they want to create it
def userConnection():
    global db_controller 

    db_name = input("Enter database name: ")
    db_exists = os.path.exists(db_name)

    if not db_exists:
        clearTerm()
        print(f"The database {db_name} does not exist. \n")
        res = input("Do you want to create it with predetermined data? (Y/N): ")
    
        if res == "N" or res == "n":
            print("Program Exited")
            return
        if res == "Y" or res == "y":
            clearTerm()
            db_controller = DBController(db_name)
            print(f"The database {db_name} has been created.")
            sleep(1)
            mainMenu()
        else:
            clearTerm()
            print(f"Invalid Input {res}.")
            userConnection()
            return

    else:
        db_controller = DBController(db_name)
        mainMenu()

# main menu that ask user for input and then goes to selected menu
def mainMenu():
    # printMainMenuOptions()
    isInvalid = False
    while True:
        printMainMenuOptions()
        if not isInvalid:
            user_selection = input("Selection: ")
        else:
            user_selection = input("Invalid Selection. Please retry: ")

        if not (isInputInt(user_selection)):
            isInvalid = True
            continue

        match int(user_selection):
            case 1:
                print("entering members menu")
                memberMenu()
                isInvalid = False
            case 2:
                print("entering classes menu")
                classMenu()
                isInvalid = False
            case 3:
                print("entering equipment menu")
                equipmentMenu()
                isInvalid = False
            case 4:
                print("Exiting Program")
                db_controller.close_connection()
                sys.exit()
            case _:
                isInvalid = True
        
# this menu allows a user to select an action (currently does not do anything, needs methods for each case)       
def memberMenu():
    clearTerm()
    isInvalid = False
    while True:
        printMemberMenuOptions()

        if not isInvalid:
            selection = input("Selection: ")
        else:
            selection = input("Invalid Selection. Please retry: ")

        if not (isInputInt(selection)):
            isInvalid = True
            continue
        
        match int(selection):
            case 1:
                clearTerm()
                getAllMembers(db_controller)
            case 2:
                clearTerm()
                addMember(db_controller)
            case 3:
                clearTerm()
                editMemberSelection(db_controller)
            case 4:
                deleteMember(db_controller)
            case 0:
                return
            case _:
                print('Invalid Selection')

# this menu allows a user to select an action (currently does not do anything, needs methods for each case)       
def  classMenu():
    
    isInvalid = False
    while True:
        printClassMenuOptions()

        if not isInvalid:
            selection = input("Selection: ")
        else:
            selection = input("Invalid Selection. Please retry: ")

        if not (isInputInt(selection)):
            isInvalid = True
            continue

        match int(selection):
            case 1:
                print("displaying classes with their attendance")
            case 2:
                print("adding new class")
            case 3:
                print("updating class")
            case 4:
                print('deleting class')
            case 5:
                print('viewing members of class')
            case 0:
                return
            case _:
                print('Invalid Selection')

# this menu allows a user to select an action (currently does not do anything, needs methods for each case)       
def equipmentMenu():
    
    isInvalid = False
    while True:
        printEquipmentMenuOptions()

        if not isInvalid:
            selection = input("Selection: ")
        else:
            selection = input("Invalid Selection. Please retry: ")

        if not (isInputInt(selection)):
            isInvalid = True
            continue
        
        match int(selection):
            case 1:
                print("showing all equipment")
            case 2:
                print("add new equipment")
            case 3:
                print("updating equipment")
            case 4:
                print("deleting equipment")
            case 0:
                return
            case _:
                print('Invalid Input')

def getdb_controller():
    return db_controller

# starting method that clears the terminal and initiates the first connection method
def main():
    clearTerm()
    print(greeting)
    userConnection()

if __name__ == "__main__":
    main()