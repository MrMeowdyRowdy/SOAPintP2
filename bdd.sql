CREATE TABLE availability (
    room_id INTEGER PRIMARY KEY,
    room_type TEXT NOT NULL,
    available_date DATE NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO availability (room_id, room_type, available_date, status)
VALUES
(1, 'Single', '2024-12-15', 'available'),
(2, 'Double', '2024-12-15', 'maintenance'),
(3, 'Suite', '2024-12-16', 'available'),
(4, 'Single', '2024-12-17', 'available'),
(5, 'Double', '2024-12-17', 'available');
