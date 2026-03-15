CREATE DATABASE demoblaze_test;

USE demoblaze_test;

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    title VARCHAR(255),
    price INT,
    category VARCHAR(100)
);

INSERT INTO products (product_id, title, price, category) VALUES
(1, 'Samsung galaxy s6', 360, 'phone'),
(2, 'Nokia lumia 1520', 820, 'phone'),
(3, 'Nexus 6', 650, 'phone'),
(4, 'Samsung galaxy s7', 800, 'phone'),
(5, 'Iphone 6 32gb', 790, 'phone'),
(6, 'Sony xperia z5', 320, 'phone'),
(7, 'HTC One M9', 700, 'phone'),
(8, 'Sony vaio i5', 790, 'notebook'),
(9, 'Sony vaio i7', 790, 'notebook'),
(11, 'MacBook air', 700, 'notebook'),
(12, 'Dell i7 8gb', 700, 'notebook'),
(13, '2017 Dell 15.6 Inch', 700, 'notebook'),
(15, 'MacBook Pro', 1100, 'notebook');