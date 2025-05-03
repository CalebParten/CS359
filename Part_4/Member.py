from DBController import DBController
from sqlite3 import Error
from sqlite3 import IntegrityError
from Format import *
    

# returns all members from database with all attributes
def getAllMembers(db_controller):
    try:

        query = '''
        SELECT Member.memberId, Member.name, Member.email, Member.phone, 
        Member.address, Member.age, Member.membershipStartDate, Member.membershipEndDate
        From Member;
        '''

        curs = db_controller.getConnection().cursor()
        curs.execute(query)
        results = curs.fetchall()
        headers = ['ID','Name','E-mail','Phone Number','Address','Age','Start Date','End Date']
        formatToTable(headers,results)
        user_input = input("Press enter to return")
        return
    
    except Error as e:
        print(e)
 
# adds a new member to the database with inputs specified by user
def addMember(db_controller):
    print("Add Member")
    try:
        name = input("Name: ")
        email = input("E-mail: ")
        phone = input("Phone Number: ")
        address = input("Address: ")
        age = input("Age: ")
        start = input("Start date (YYYY-MM-DD): ")
        end = input("End date (YYYY-MM-DD): ")

        query = '''
        INSERT INTO Member (name,email,phone,address,age,membershipStartDate,membershipEndDate)
        Values (?,?,?,?,?,?,?);
        '''

        member_parameters = (name,email,phone,address,age,start,end)
        curs = db_controller.getConnection().cursor()
        curs.execute(query,member_parameters)
        db_controller.getConnection().commit()

        headers = ['Name','E-mail','Phone Number','Address','Age','Start Date','End Date']
        results = [[name,email,phone,address,age,start,end]]
        formatToTable(headers,results)

        print("This Member has been added to the database.")
        user_input = input("Press enter to return")
        return
    
    except Error as e:
        if 'membershipEndDate > membershipStartDate' in str(e):
            print('Error: (2 possible)')
            print('1. One or both of the provided dates were formatted incorrectly.')
            print('2. The start date occurs after the end date.')
            input("Press enter to return")

# allows user to select a member to edit
def editMemberSelection(db_controller):
    print("Edit Member")
    print('-'*80)
    isInvalid = False
    while True:

        if not isInvalid:
            member_id = input("Enter the Member ID (0 to return): ")
        else:
            member_id = input("Invalid Member ID. Please retry (0 to return): ")

        if not isInputInt(member_id):
            isInvalid = True
            continue

        if member_id == '0':
            return


        member_info = getMember(db_controller, member_id)
        headers = ['ID','Name','E-mail','Phone Number','Address','Age','Start Date','End Date']

        if not member_info:
            print(f"Cannot find Member with ID {member_id}")
            isInvalid = False
            continue
        else:
            editMember(db_controller, member_info, member_id, headers)
            return

# edits a member in a table by allowing user to select wich attribute to edit
def editMember(db_controller, member_info, member_id, headers):

    isInvalid = False
    while True:
        clearTerm()
        formatToTable(headers, member_info)
        print("\n")
        print("Which attribute would you like to change?")
        print("1. Name")
        print("2. E-mail")
        print('3. Phone Number')
        print('4. Address')
        print('5. Age')
        print('6. Start Date')
        print('7. End Date')

        if not isInvalid:
            selected_attr = input("Select the attribute you want to change (0 to return): ")
        else:
            selected_attr = input("Invalid Selection. Please retry (0 to return): ")
        
        if selected_attr == '0':
            return
        
        if not isInputInt(selected_attr):
            isInvalid = True
            continue
        
        attr_dict = {
            '1': 'name',
            '2': 'email',
            '3': 'phone',
            '4': 'address',
            '5': 'age',
            '6': 'membershipStartDate',
            '7': 'membershipEndDate'
        }
        new_attr_value = input("Enter the new value: ")

        try:
            if (attr_dict.get(selected_attr) == 'age') and (not isInputInt(new_attr_value)):
                print("Age attribute must be an integer.")
                input("Press enter to return")
                continue

            query = f'''
            UPDATE Member
            SET {attr_dict.get(selected_attr)} = ?
            WHERE memberId = ?;
            '''
            params = [new_attr_value,member_id]
            curs = db_controller.getConnection().cursor()
            curs.execute(query,params)
            db_controller.getConnection().commit()

            clearTerm()
            updated_member = getMember(db_controller,member_id)
            formatToTable(headers, updated_member)
            print("Member has been updated.")
            input("Press enter to return")
            return
        
        except Error as e:
            if 'membershipEndDate > membershipStartDate' in str(e):
                print('Error: (2 possible)')
                print('1. One or both of the provided dates were formatted incorrectly.')
                print('2. The start date occurs after the end date.')
                input('Press enter to return')
                continue
            if 'age >= 15' in str(e):
                print('Error: Age must be greater than 15')
                input('Press enter to return')
                continue
            print(e)



def getMember(db_controller, member_id):

    try:
        query = '''
        SELECT Member.memberId, Member.name, Member.email, Member.phone, 
        Member.address, Member.age, Member.membershipStartDate, Member.membershipEndDate
        FROM Member WHERE memberId = ?;
        '''
        curs = db_controller.getConnection().cursor()
        param = [member_id]
        curs.execute(query,param)
        results = curs.fetchall()
        return results
    
    except Error as e:
        print(e)



# allows the user to select a member to delete with the id
def deleteMemberSelect(db_controller):
    clearTerm()
    print("Delete Member")
    print('-'*80)
    isInvalid = False
    while True:
        
        if not isInvalid:
            member_id = input("Enter the Member ID (0 to return): ")
        else:
            member_id = input("Invalid Member ID. Please retry (0 to return): ")
        
        if not isInputInt(member_id):
            isInvalid = True
            continue

        if member_id == '0':
            return
        
        member_info = getMember(db_controller, member_id)
        headers = ['ID','Name','E-mail','Phone Number','Address','Age','Start Date','End Date']

        if not member_info:
            print(f"Cannot find Member with ID {member_id}")
            isInvalid = False
            continue
        
        clearTerm()
        formatToTable(headers,member_info)
        print("/n")
        print(f"Please confirm the deletion of member with ID {member_id}")
        confirmation = input("Confirmation (yes/no): ")

        if confirmation == 'yes' or confirmation == 'Yes':
            deleteMember(db_controller,member_info,member_id,headers)
            return
        elif confirmation == 'no' or confirmation == 'No':
            return
    
        else:
            print("Invalid Confirmation.")
            print("Press enter to return")
            continue
        
        

# deletes a member from table with it's id (deletes records of member from other tables as well)
def deleteMember(db_controller, member_info, member_id, headers):
    clearTerm()
    try:
        query = f'''
        DELETE FROM Member
        WHERE memberId = ?;
        '''
        curs = db_controller.getConnection().cursor()
        param = [member_id]
        curs.execute(query,param)
        db_controller.getConnection().commit()
        
        formatToTable(headers,member_info)
        print(f"Member with ID {member_id} has been deleted.")
        input('Press enter to return')
        return
    except Error as e:
        print(e)
        input("Press enter to return")
        return


            



