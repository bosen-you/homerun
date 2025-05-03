CREATE DATABASE IF NOT EXISTS image_db;
USE image_db;

-- create a table
CREATE TABLE IF NOT EXISTS static (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- test
SELECT * FROM static;

DELETE FROM static