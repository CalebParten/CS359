import sqlite3
from Format import *  # Assumes you have a formatToTable function in Format.py

# Fetch and display all classes. Optionally includes attendance data.
def getAllClasses(db_controller, skip_conf=False):
    conn = db_controller.getConnection()
    cursor = conn.cursor()

    try:
        if skip_conf:
            # Basic class info without attendance (used for internal selection)
            cursor.execute("""
                SELECT classId, className, classType, duration, classCapacity, instructorId, gymId
                FROM Class
            """)
            headers = ["Class ID", "Name", "Type", "Duration", "Capacity", "Instructor ID", "Gym ID"]
        else:
            # Class info with count of members attending
            cursor.execute("""
                SELECT 
                    c.classId, c.className, c.classType, c.duration, 
                    c.classCapacity, c.instructorId, c.gymId,
                    COUNT(a.memberId) as attendanceCount
                FROM Class c
                LEFT JOIN Attends a ON c.classId = a.classId
                GROUP BY c.classId
            """)
            headers = ["Class ID", "Name", "Type", "Duration", "Capacity", "Instructor ID", "Gym ID", "Attendees"]

        results = cursor.fetchall()

        # Display results as a formatted table
        print("\nAll Classes:")
        formatToTable(headers, results)
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")

    # Only pause for user input if this was a direct call, not an internal helper
    if not skip_conf:
        input("\nPress Enter to continue...")

# Add a new class to the database
def addClass(db_controller):
    conn = db_controller.getConnection()
    cursor = conn.cursor()

    # Gather input from user
    className = input("Enter Class Name: ")
    classType = input("Enter Class Type (Yoga, Zumba, HIIT, Weights): ")
    duration = int(input("Enter Duration (in minutes): "))
    classCapacity = int(input("Enter Class Capacity: "))
    instructorId = input("Enter Instructor ID (or leave blank): ") or None
    gymId = input("Enter Gym ID (or leave blank): ") or None

    try:
        # Insert new class record
        cursor.execute("""
            INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (className, classType, duration, classCapacity, instructorId, gymId))
        conn.commit()
        print("Class added successfully.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")
    
    input("\nPress Enter to continue...")

# Update an existing class
def updateClass(db_controller):
    conn = db_controller.getConnection()
    cursor = conn.cursor()

    # Show current classes without attendance info
    getAllClasses(db_controller, skip_conf=True)
    classId = input("Enter Class ID to update: ")

    try:
        # Fetch class to update
        cursor.execute("SELECT * FROM Class WHERE classId = ?", (classId,))
        cls = cursor.fetchone()

        if not cls:
            print("Class not found.")
            return

        # Prompt user for new values (press Enter to keep old)
        print(f"Editing Class: {cls}")
        className = input(f"New name (leave blank to keep '{cls[1]}'): ") or cls[1]
        classType = input(f"New type (leave blank to keep '{cls[2]}'): ") or cls[2]
        duration = input(f"New duration (leave blank to keep '{cls[3]}'): ") or cls[3]
        classCapacity = input(f"New capacity (leave blank to keep '{cls[4]}'): ") or cls[4]
        instructorId = input(f"New instructor ID (leave blank to keep '{cls[5]}'): ") or cls[5]
        gymId = input(f"New gym ID (leave blank to keep '{cls[6]}'): ") or cls[6]

        # Update the record
        cursor.execute("""
            UPDATE Class SET className = ?, classType = ?, duration = ?, classCapacity = ?, instructorId = ?, gymId = ?
            WHERE classId = ?
        """, (className, classType, duration, classCapacity, instructorId, gymId, classId))
        conn.commit()
        print("Class updated.")
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")

    input("\nPress Enter to continue...")

# Delete a class (with safeguard if members are still registered)
def deleteClass(db_controller):
    conn = db_controller.getConnection()
    cursor = conn.cursor()

    # Show classes to choose from
    getAllClasses(db_controller, skip_conf=True)
    classId = input("Enter Class ID to delete: ")

    try:
        # Make sure the class exists
        cursor.execute("SELECT * FROM Class WHERE classId = ?", (classId,))
        if cursor.fetchone() is None:
            print(f"No class found with ID {classId}")
            input("\nPress Enter to continue...")
            return

        # Check if there are attendees in this class
        cursor.execute("SELECT COUNT(*) FROM Attends WHERE classId = ?", (classId,))
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Class {classId} has {count} registered member(s).")
            choice = input("Do you want to move them to another class before deletion? (Y/N): ").strip().lower()

            if choice == 'y':
                newClassId = input("Enter the ID of the class to move members to: ")

                # Verify new class exists
                cursor.execute("SELECT * FROM Class WHERE classId = ?", (newClassId,))
                if cursor.fetchone() is None:
                    print(f"No class found with ID {newClassId}. Aborting.")
                    input("\nPress Enter to continue...")
                    return

                # Migrate members to new class
                cursor.execute("""
                    UPDATE Attends SET classId = ?
                    WHERE classId = ?
                """, (newClassId, classId))
                conn.commit()
                print(f"Moved members to class {newClassId}.")
            else:
                print("Aborting deletion to preserve member registrations.")
                input("\nPress Enter to continue...")
                return

        # Safe to delete class now
        cursor.execute("DELETE FROM Class WHERE classId = ?", (classId,))
        conn.commit()
        print(f"Class {classId} has been deleted.")

    except sqlite3.Error as e:
        print(f"[ERROR] {e}")

    input("\nPress Enter to continue...")

# List all members of a class
def getClassMembers(db_controller):
    conn = db_controller.getConnection()
    cursor = conn.cursor()

    # Display classes for user to choose from
    getAllClasses(db_controller, skip_conf=True)
    classId = input("Enter Class ID to view members: ")

    try:
        # Query all members and their attendance date for the given class
        cursor.execute("""
            SELECT m.memberId, m.name, a.attendanceDate
            FROM Member m
            JOIN Attends a ON m.memberId = a.memberId
            WHERE a.classId = ?
            ORDER BY a.attendanceDate DESC
        """, (classId,))
        results = cursor.fetchall()
        headers = ["Member ID", "Name", "Last Attendance"]

        # Display the result as a table
        print(f"\nMembers in Class {classId}:")
        formatToTable(headers, results)
    except sqlite3.Error as e:
        print(f"[ERROR] {e}")

    input("\nPress Enter to continue...")
