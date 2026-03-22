CREATE DATABASE canteen_db;
USE canteen_db;

CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50)
);

CREATE TABLE Menu (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(50),
    price DECIMAL(5,2)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    item_id INT,
    quantity INT,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (item_id) REFERENCES Menu(item_id)
);

CREATE TABLE Tokens (
    token_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    token_number INT,
    status VARCHAR(20),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

INSERT INTO Students VALUES
(1, 'Arun', 'CSE'),
(2, 'Meena', 'ECE'),
(3, 'Rahul', 'MECH'),
(4, 'Anu', 'CSE'),
(5, 'John', 'EEE');

INSERT INTO Menu VALUES
(1, 'Burger', 50),
(2, 'Pizza', 100),
(3, 'Sandwich', 40),
(4, 'Tea', 10),
(5, 'Coffee', 20),
(6, 'Juice', 30),
(7, 'Dosa', 35),
(8, 'Fried Rice', 80);
