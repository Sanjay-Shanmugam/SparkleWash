DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS users;

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    duration_minutes INTEGER NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user', -- 'user' or 'admin'
    vehicle_no VARCHAR(50),
    vehicle_type VARCHAR(50)
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    booking_date VARCHAR(50) NOT NULL,
    start_time VARCHAR(50) NOT NULL,
    end_time VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);

INSERT INTO services (name, description, price, duration_minutes) VALUES
('Basic Wash', 'Exterior wash and dry', 10.00, 30),
('Premium Wash', 'Exterior wash, wax, and interior vacuum', 25.00, 60),
('Deluxe Detail', 'Full detail including polishing and interior shampoo', 50.00, 120);

-- Insert a default admin for testing (password: admin123)
INSERT INTO users (name, email, phone, password_hash, role, vehicle_no, vehicle_type) VALUES 
('Admin User', 'admin@sparklewash.com', '000-000-0000', 'scrypt:32768:8:1$lR5r5L5S5e5a5m$6250646039525c34535f5c5061695f3661646d696e313233', 'admin', 'ADMIN', 'None');
