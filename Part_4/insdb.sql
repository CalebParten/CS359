INSERT INTO Member (name,email,phone,address,age,membershipStartDate,membershipEndDate) VALUES
    ('David Schmith', 'ds@mail.com',9998887777, '124 Fake St. Nonexistent,NA 00000', 21, '2025-03-01', '2026-03-01'),
    ('Mario Soto', 'ms@mail.com', 5552225555, '125 Fake St. Nonexistent, NA 00000', 21, '2025-03-01', '2026-03-01'),
    ('Caleb Parten', 'cp@mail.com',8887776666, '126 Fake St. Nonexistent,NA 00000', 20, '2025-03-01', '2026-03-01'),
    ('Adraine Caldwell', 'ac@mail.com',5554443333, '127 Fake St. Nonexistent,NA 00000', 22, '2025-03-01', '2026-03-01'),
    ('Eduardo Ceh Varela', 'ecv@mail.com', 7771117777, '128 Fake St. Nonexistent,NA 00000', 42, '2025-03-02', '2026-03-02'),
    ('Benjamin Caldwell', 'bc@mail.com', 9991112222, '129 Fake St. Nonexistent, NA 00000', 25, '2025-03-01','2025-04-01'),
    ('Austin Johnson', 'aj@mail.com', 5554444111, '130 Fake St. Nonexistent, NA 00000', 24, '2025-03-01','2025-04-01');
    
INSERT INTO Instructor (name, specialty, phone, email) VALUES
    ('Jacob Smith', 'Yoga', 1112223333, 'js@mail.com'),
    ('Mary Johnson', 'Zumba', 2223334444, 'mj@mail.com'),
    ('Tom Jacobson', 'HIIT', 3334445555, 'tj@mail.com'),
    ('Joseph Gonzales', 'Weights', 4445556666, 'jg@mail.com'),
    ('Bob Brown', 'Weights', 5556667777,'bb@mail.com');

INSERT INTO GymFacility (location, phone, manager) VALUES
    ('Portales NM', 4441112222, 'Thomas Pritchett'),
    ('Clovis NM', 5552223333, 'Kayla Stevenson'),
    ('Roswell NM', 6663332222, 'Caroline Wall'),
    ('Ruidoso NM', 7774445555, 'Corny Friesen'),
    ('Melrose NM', 8885556666, 'Peter Froese');

INSERT INTO MembershipPlan (planType, cost) VALUES
    ('Monthly', 50.00),
    ('Annual', 500.00),
    ('Monthly', 25.00),
    ('Annual' , 250.00),
    ('Annual', 750.00);
    
INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId) VALUES
    ('Morning Yoga', 'Yoga', 60, 20, 1, 1),
    ('Zumba Dance', 'Zumba', 45, 25, 2, 2),
    ('HIIT Blast', 'HIIT', 30, 15, 1, 3),
    ('Strength Training', 'Weights', 75, 10, 4, 4),
    ('Afternoon Yoga', 'Yoga', 60, 20, 5, 5);

INSERT INTO Equipment (name, type, quantity, gymId) VALUES
    ('Treadmills', 'Cardio', 5, 1),
    ('Dumbbells', 'Strength', 20, 2),
    ('Resistance Bands', 'Flexibility', 15, 3),
    ('Foam Rollers', 'Recovery', 10, 4),
    ('Elliptical', 'Cardio', 3, 5);
    
INSERT INTO Payment (memberId, planId, amountPaid, paymentDate) VALUES
    (1, 1, 50.00, '2025-03-01'),
    (2, 2, 500.00,'2025-03-01'),
    (3, 3, 25.00, '2025-03-01'),
    (4, 4, 250.00, '2025-03-01'),
    (5, 5, 750.00, '2025-03-01');

INSERT INTO Attends (memberId, classId, attendanceDate) VALUES
    (1,2,'2025-04-02'),
    (1,4,'2025-04-02'),
    (2,1,'2025-03-02'),
    (3,4,'2025-04-02'),
    (4,3,'2025-03-02'),
    (5,2,'2025-03-02');