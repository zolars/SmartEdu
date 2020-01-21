CREATE DATABASE smartedu;
USE smartedu;

CREATE TABLE user_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(10) UNIQUE NOT NULL,
  password VARCHAR(20) NOT NULL,
  role BOOLEAN NOT NULL,
  reg_ip VARCHAR(16) NOT NULL,
  reg_time TIMESTAMP NOT NULL,
  mobile VARCHAR(12) NOT NULL,
  birthday TIMESTAMP NOT NULL,
  province VARCHAR(10) DEFAULT NULL,
  city VARCHAR(10) DEFAULT NULL, 
  gender BOOLEAN DEFAULT NULL,
  customer_name VARCHAR(10) DEFAULT NULL,
  student_id VARCHAR(11) DEFAULT NULL,
  mail VARCHAR(20) DEFAULT NULL,
  signature VARCHAR(50) DEFAULT NULL,
  id_active BOOLEAN DEFAULT NULL,
  id_alive BOOLEAN DEFAULT 0
);