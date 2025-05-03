from DBController import DBController
from sqlite3 import Error
from sqlite3 import IntegrityError
from Format import *

# Fetches and displays all equipment records from the database
def getAllEquipment(db_controller):

    try:

        query = '''
        SELECT Equipment.equipmentId, Equipment.name, Equipment.type, Equipment.quantity, GymFacility.location
        From Equipment
        LEFT JOIN GymFacility ON Equipment.gymId = GymFacility.gymId
        '''

        curs = db_controller.getConnection().cursor()
        curs.execute(query)
        results = curs.fetchall()
        headers = ['ID', 'Name','Type', 'Quantity', 'Gym Location']
        formatToTable(headers, results)
        input("Press enter to return")

    except Error as e:
        print(e)

# Adds a new equipment entry to the database
def addEquipment(db_controller):
    print("Add Equipment")
    try:
        name = input("Name: ")
        type = input("Type (Cardio / Strength / Flexibility / Recovery): ")
        quantity = input("Quantity: ")
        gym_id = input("GYM ID: ")

        query = '''
        INSERT INTO Equipment (name, type, quantity, gymId)
        VALUES (?, ?, ?, ?);
        '''
        
        equipment_params = (name, type, quantity, gym_id)
        curs = db_controller.getConnection().cursor()
        curs.execute(query, equipment_params)
        db_controller.getConnection().commit()

        headers = ['Name', 'Type', 'Quantity', 'Gym ID']
        results = [[name, type, quantity, gym_id]]
        formatToTable(headers, results)
        print("Equipment added successfully.")
        input("Press enter to return")

    except Error as e:
        print("Error adding equipment:", e)
        input("Press enter to return")

# Prompts user to select an equipment entry by ID and proceed to edit it
def editEquipmentSelection(db_controller):
    print("Edit Equipment")
    print('-' * 80)
    isInvalid = False
    while True:
        equipment_id = input("Enter Equipment ID (0 to return): ") if not isInvalid else input("Invalid ID. Try again (0 to return): ")

        if not isInputInt(equipment_id):
            isInvalid = True
            continue
        if equipment_id == '0':
            return

        equipment_info = getEquipment(db_controller, equipment_id)
        headers = ['ID', 'Name', 'Type', 'Quantity', 'Gym ID']

        if not equipment_info:
            print(f"Cannot find Equipment with ID {equipment_id}")
            isInvalid = True
            continue
        else:
            editEquipment(db_controller, equipment_info, equipment_id, headers)
            return

# Edits a specific attribute (name, type, quantity, gymId) of a selected equipment entry      
def editEquipment(db_controller, equipment_info, equipment_id, headers):
    isInvalid = False
    attr_dict = {
        '1': 'name',
        '2': 'type',
        '3': 'quantity',
        '4': 'gymId'
    }

    while True:
        clearTerm()
        formatToTable(headers, [equipment_info])
        print("\nWhich attribute would you like to update?")
        print("1. Name")
        print("2. Type")
        print("3. Quantity")
        print("4. Gym ID")

        selected_attr = input("Select (0 to return): ") if not isInvalid else input("Invalid selection. Try again (0 to return): ")

        if selected_attr == '0':
            return
        if selected_attr not in attr_dict:
            isInvalid = True
            continue

        new_value = input("Enter new value: ")

        try:
            query = f'''
            UPDATE Equipment
            SET {attr_dict[selected_attr]} = ?
            WHERE equipmentId = ?;
            '''
            params = (new_value, equipment_id)
            curs = db_controller.getConnection().cursor()
            curs.execute(query, params)
            db_controller.getConnection().commit()
            print("Update successful.")
            input("Press enter to return")
            return
        except Error as e:
            print("Update failed:", e)
            input("Press enter to return")
            return

# Retrieves a single equipment entry by ID
def getEquipment(db_controller, equipment_id):
    try:
        query = '''
        SELECT equipmentId, name, type, quantity, gymId
        FROM Equipment
        WHERE equipmentId = ?;
        '''
        curs = db_controller.getConnection().cursor()
        curs.execute(query, [equipment_id])
        return curs.fetchone()
    except Error as e:
        print(e)
        return None

#  Deletes an equipment entry by ID
def deleteEquipment(db_controller):
    print("Delete Equipment")
    equipment_id = input("Enter Equipment ID to delete (0 to cancel): ")
    if not isInputInt(equipment_id) or equipment_id == '0':
        return

    try:
        query = "DELETE FROM Equipment WHERE equipmentId = ?;"
        curs = db_controller.getConnection().cursor()
        curs.execute(query, [equipment_id])
        db_controller.getConnection().commit()
        print("Equipment deleted.")
        input("Press enter to return")
    except Error as e:
        print("Failed to delete:", e)
        input("Press enter to return")


