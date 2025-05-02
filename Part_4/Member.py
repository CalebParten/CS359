from DBController import DBController
from sqlite3 import Error
from sqlite3 import IntegrityError
    

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
        if isinstance(e, IntegrityError):
            print('Error: (2 possible)')
            print('1. One or both of the provided dates were formatted incorrectly.')
            print('2. The start date occurs after the end date.')
            input("Press enter to return")

    
    
    
def editMember(db_controller):
    print("Edit Member")

def deleteMember(db_controller):
    print("Delete Member")
    

def formatToTable(headers, results):

    column_widths = [0]*len(headers)
    temp_results = results.copy()
    temp_results.append(tuple(headers))
    total_width = 0

    for row in temp_results:
        for index, item in enumerate(row):
            if len(str(item)) > column_widths[index]:
                column_widths[index] = len(str(item))
            
    for value in column_widths:
        total_width += value

    border = '+-'
    for index, header in enumerate(headers):
        border += ('-'*column_widths[index]) + '-+-'
    print(border)

    title = '| '
    for index, header in enumerate(headers):
        title += f'{header:<{column_widths[index]}} | '
    print(title)
    print(border)
    
    for row in results:
        row_string = '| '
        for index, item in enumerate(row):
            row_string += f'{item:<{column_widths[index]}} | '
        print(row_string)

    print(border)
    return

