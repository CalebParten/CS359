CREATE TABLE Member (
    memberId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(100),
    age INTEGER CHECK (age >= 15),
    membershipStartDate DATE NOT NULL,
    membershipEndDate DATE NOT NULL CHECK(membershipEndDate > membershipStartDate)
);

CREATE TABLE Class (
    classId INTEGER PRIMARY KEY AUTOINCREMENT,
    className VARCHAR(50),
    classType VARCHAR(20) CHECK(classType IN ('Yoga', 'Zumba', 'HIIT', 'Weights')),
    duration INTEGER CHECK (duration > 0),
    classCapacity INTEGER CHECK(classCapacity > 0),
    instructorId INTEGER,
    gymId INTEGER,
    FOREIGN KEY (instructorId) REFERENCES Instructor(instructorId),
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId)
);

CREATE TABLE Instructor (
    instructorId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    specialty VARCHAR(50),
    phone VARCHAR(15),
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE GymFacility (
    gymId INTEGER PRIMARY KEY AUTOINCREMENT,
    location varchar(100),
    phone varchar(30),
    manager varchar(50)
);

CREATE TABLE Equipment (
    equipmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(30) CHECK(type = 'Cardio' OR type = 'Strength' OR type = 'Flexibility' OR type = 'Recovery'),
    quantity INTEGER CHECK (quantity >= 0),
    gymId INTEGER,
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId)
);

CREATE TABLE MembershipPlan (
    planId INTEGER PRIMARY KEY AUTOINCREMENT,
    planType VARCHAR(20) CHECK(planType IN('Monthly', 'Annual')),
    cost NUMERIC CHECK (cost >= 0)
);

CREATE TABLE Payment (
    paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberId INTEGER,
    planId INTEGER,
    amountPaid REAL NOT NULL CHECK(amountPaid >= 0),
    paymentDate DATE NOT NULL,
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (planId) REFERENCES MembershipPlan(planId)
);

CREATE TABLE Attends (
    memberId INTEGER,
    classId INTEGER,
    attendanceDate DATE NOT NULL,
    PRIMARY KEY (memberId, classId, attendanceDate),
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (classId) REFERENCES Class(classId)
);