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
