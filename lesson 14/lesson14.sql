-- 1. Подготовка базы данных
CREATE DATABASE IF NOT EXISTS lesson14;
USE lesson14;

-- 2. Удаление старых таблиц (в обратном порядке из-за связей)
-- Это нужно, чтобы скрипт можно было запускать много раз без ошибок
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS seller;
DROP TABLE IF EXISTS users;

-- 3. Таблица пользователей (users)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- 4. Таблица продавцов (seller)
CREATE TABLE seller (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    phone VARCHAR(20)
);

-- 5. Таблица товаров (products)
-- Связана с таблицей seller через seller_id
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cost INT NOT NULL,
    count INT NOT NULL,
    seller_id INT,
    FOREIGN KEY (seller_id) REFERENCES seller(id) ON DELETE CASCADE
);

-- 6. Таблица заказов (orders)
-- Связывает пользователей (user_id) и товары (product_id)
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    count INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

