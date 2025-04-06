import sqlite3
from sqlite3 import Error
import sys
import os

# Connects to the database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("[INFO] Connection established: " + sqlite3.sqlite_version)

    except Error as e:
        print(e)

    return conn

# Closes the connection to the database
def close_connection(conn):
    conn.close()
    print("[INFO] Connection Terminated: " + sqlite3.sqlite_version)


# Initiates the database if it doesn't already exist
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

# Inserts data from the insdb.sql file
def insert_data(conn):
    raw_insdb = open("insdb.sql")
    script_insdb = raw_insdb.read()

    try:
        curs = conn.cursor()
        curs.executescript(script_insdb)
        print("Data Inserted into Tables")
    except Error as e:
        print(e)

# This method acts as a switch statement for the command line
# argument that is provided by the user.
def query_selection(number, conn):
    if(number == 1):
        query_all_members_with_plans(conn)
    elif(number == 2):
        query_class_count_per_gym(conn)
    elif(number == 3):
        query_members_by_class(conn)
    elif(number == 4):
        query_equipment_type(conn)
    elif (number == 5):
        query_expired_memberships(conn)
    elif (number == 6):
        query_classes_taught(conn)
    elif (number == 7):
        calcAvgMemAge(conn)
    elif (number == 8):
        findTopInst(conn)
    elif (number == 9):
        findMembForClassType(conn)
    elif (number == 10):
        getMemAttendLastMonth(conn)
    else:
        print("error: argument was not valid")
    

# -----------------------------------------------------------
# Numbered methods below query the database to obtain the 
# proper output correlating with their number
# -----------------------------------------------------------

# 1.
def query_all_members_with_plans(input):
    conn = input[0]
    print("Query 1: All gym members with their membership plan")
    try:
        query = '''
        SELECT Member.name, Member.email, Member.age, MembershipPlan.planType
        FROM Member
        JOIN Payment ON Member.memberId = Payment.memberId
        JOIN MembershipPlan ON Payment.planId = MembershipPlan.planId;
        '''
        curs = conn.cursor()
        curs.execute(query)
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(e)

# 2
def query_class_count_per_gym(input):
    conn = input[0]
    print("Query 2: Number of classes at each gym")
    try:
        query = '''
        SELECT GymFacility.location, COUNT(Class.classId) AS classCount
        FROM GymFacility
        LEFT JOIN Class ON GymFacility.gymId = Class.gymId
        GROUP BY GymFacility.gymId;
        '''
        curs = conn.cursor()
        curs.execute(query)
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(e)

# 3
def query_members_by_class(input):
    conn = input[0]
    class_id = input[1]
    print(f"Query 3: Members attending class {class_id}")
    try:
        query = '''
        SELECT Member.name
        FROM Member
        JOIN Attends ON Member.memberId = Attends.memberId
        WHERE Attends.classId = ?;
        '''
        curs = conn.cursor()
        curs.execute(query, (class_id,))
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(e)

# 4
def query_equipment_type(input):
    conn = input[0]
    equipment_type = input[1]
    print(f"Query 4: List of all equipment of a specific type")
    try:
        query = '''
            SELECT Equipment.name, Equipment.type, Equipment.quantity
            FROM Equipment
            WHERE type = ?
        '''
        curs = conn.cursor()
        curs.execute(query, (equipment_type,))
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print("An error occurred:", e)

# 5
def query_expired_memberships(input):
    conn = input[0]
    print(f"Query 5: Members with expired memberships")
    try:
        query = '''
            SELECT Member.name, Member.membershipEndDate
            FROM Member
            WHERE DATE(membershipEndDate) < DATE('now')
        '''
        curs = conn.cursor()
        curs.execute(query)
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print("An error occurred:", e)

# 6
def query_classes_taught(input):
    conn = input[0]
    instructorId = input[1]
    print(f"Query 6: Classes taught by a specific instructor")
    try:
        query = '''
            SELECT Instructor.name, Instructor.phone, Class.className, Class.classType, Class.duration, Class.classCapacity
            FROM Class
            JOIN Instructor ON Class.instructorId = Instructor.instructorId
            WHERE Instructor.instructorId = ?;
        '''
        curs = conn.cursor()
        curs.execute(query, (instructorId,))
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print("An error occurred:", e)

# 7
def calcAvgMemAge(input):
    conn = input[0]
    print("Query 7: Average of all active and past members")
    try:
        query = '''
        Select
        (Select avg(Member.age)
         From Member
         Where Member.membershipEndDate > CURRENT_DATE),
        (Select avg(Member.age)
         From Member
         Where Member.membershipEndDate < CURRENT_DATE);
        '''
        curs = conn.cursor()
        curs.execute(query)
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(e)

# 8
def findTopInst(input):
    conn = input[0]
    print("Query 7: Find top three intructors who teach the most classes")
    try:
        query = '''
        Select Instructor.name, Instructor.instructorId ,COUNT(Class.classId) AS classCount
        From Instructor
        JOIN Class ON Instructor.instructorId = Class.instructorId
        GROUP BY Instructor.instructorId
        ORDER BY classCount DESC
        LIMIT 3;
        '''
        curs = conn.cursor()
        curs.execute(query)
        results = curs.fetchall()
        for row in results:
            print(row)
    except Error as e:
        print(e)

# 9
def findMembForClassType(input):
    conn = input[0]
    classType = input[1]
    print("Query 9: Find all members that have attended a specified class type")
    try:
        query = '''
        Select Member.memberId, Member.name
        From Attends
        JOIN Member ON Attends.memberId = Member.memberId
        JOIN Class ON Attends.classId = Class.classId
        Where Class.classType = "'''+classType+'''";
        '''
        curs = conn.cursor()
        curs.execute(query)
        results = curs.fetchall()
        for row in results:
            print(row)

    except Error as e:
        print(e)

# 10
def getMemAttendLastMonth(input):
    conn = input[0]
    print("Query 10: Find all members that have attended a class in the last month")
    try:
        query = '''
        Select 
            Member.memberId,
            Member.name,
            COUNT(Class.className) as classCount,
            GROUP_CONCAT(Class.className, ', ') AS classNames,
            GROUP_CONCAT(Class.classType, ', ') AS classTypes
        FROM Attends
        JOIN Member ON Attends.memberId = Member.memberId
        JOIN Class on Attends.classId = Class.classId
        WHERE strftime('%m',Attends.attendanceDate) = strftime('%m', CURRENT_DATE)
          AND strftime('%Y',Attends.attendanceDate) = strftime('%Y', CURRENT_DATE)
        GROUP BY Member.memberId
        ORDER BY classCount DESC;
        '''
        curs = conn.cursor()
        curs.execute(query)
        results = curs.fetchall()
        formatToTable(results)
    except Error as e:
        print(e)
    
# Formats output for question 10 into a table
def formatToTable(result):
    if result:
        print(f"{'Member Name':<30}{'Total Classes Attended':<25}{'Classes Attended':<35}{'Class Types'}\n"+"="*130)
        for row in result:
            print(f"{row[1]:<30}{row[2]:<25}{row[3]:<35}{row[4]:<40}")
    else:
        print("No result")


# Checks to see if database exists. If it does not exist, method called
# will create the database aswell as initiate rows for tables.        
def main():
    db_file="XYZGym.sqlite"
    db_exists = os.path.exists(db_file)
    conn = create_connection(db_file)
    
    if not db_exists:
        create_database(conn)
        insert_data(conn)

    if conn is not None:
        variable = ""
        command_num = sys.argv[1]
        if len(sys.argv) == 3:
            variable = sys.argv[2]
        input = [conn,variable]
        query_selection(int(command_num), input)

        close_connection(conn)

if __name__ == "__main__":
    main()
