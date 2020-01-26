CREATE DATABASE smartedu;
USE smartedu;

CREATE TABLE user_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(10) UNIQUE NOT NULL,
  password VARCHAR(20) NOT NULL,
  role BOOLEAN NOT NULL,
  reg_ip VARCHAR(16) NOT NULL,
  reg_time TIMESTAMP NOT NULL,
  birthday TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  mobile VARCHAR(12) DEFAULT NULL,
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

CREATE TABLE res_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  context VARCHAR(255) NOT NULL,
  chapter INT NOT NULL,
  difficulty INT NOT NULL,
  enter_user INT NOT NULL, 
  FOREIGN KEY (enter_user) REFERENCES user_info (id),
  enter_time TIMESTAMP NOT NULL,
  title VARCHAR(255) NOT NULL,
  type VARCHAR(10) NOT NULL,
  rating INT NOT NULL,
  description VARCHAR(255) DEFAULT NULL,
  duration INT DEFAULT NULL
);

CREATE TABLE exe_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  context_prob VARCHAR(255) NOT NULL,
  context_ans VARCHAR(255) NOT NULL,
  chapter INT NOT NULL,
  difficulty INT NOT NULL,
  enter_user INT NOT NULL,
  enter_time TIMESTAMP NOT NULL
);

CREATE TABLE hw_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  context VARCHAR(255) NOT NULL,
  chapter INT NOT NULL,
  difficulty INT NOT NULL,
  enter_user INT NOT NULL,
  enter_time TIMESTAMP NOT NULL,
  week VARCHAR(50) NOT NULL
);

CREATE TABLE page_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(50) NOT NULL
);

CREATE TABLE user_auth_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  user_ip VARCHAR(16) NOT NULL,
  operation INT NOT NULL,
  time TIMESTAMP NOT NULL,
  parent VARCHAR(255) DEFAULT NULL,
  os VARCHAR(255) DEFAULT NULL,
  browser VARCHAR(255) DEFAULT NULL,
  resolution VARCHAR(255) DEFAULT NULL
);

CREATE TABLE res_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES user_info (id),
  user_ip VARCHAR(16) NOT NULL,
  res_id INT NOT NULL, 
  FOREIGN KEY (res_id) REFERENCES res_info (id),
  operation INT NOT NULL,
  time TIMESTAMP NOT NULL,
  parent VARCHAR(255) DEFAULT NULL,
  rating INT DEFAULT NULL,
  difficulty INT DEFAULT NULL
);

CREATE TABLE exe_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES user_info (id),
  user_ip VARCHAR(16) NOT NULL,
  exe_id INT NOT NULL, 
  FOREIGN KEY (exe_id) REFERENCES exe_info (id),
  action INT NOT NULL,
  time TIMESTAMP NOT NULL,
  parent VARCHAR(255) DEFAULT NULL,
  difficulty INT DEFAULT NULL,
  answer_easy_if INT DEFAULT NULL
);

CREATE TABLE hw_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES user_info (id),
  user_ip VARCHAR(16) NOT NULL,
  hw_id INT NOT NULL, 
  FOREIGN KEY (hw_id) REFERENCES hw_info (id),
  action INT NOT NULL,
  time TIMESTAMP NOT NULL,
  context VARCHAR(255) DEFAULT NULL
);

CREATE TABLE page_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES user_info (id),
  user_ip VARCHAR(16) NOT NULL,
  page_id INT NOT NULL, 
  FOREIGN KEY (page_id) REFERENCES page_info (id),
  time TIMESTAMP NOT NULL
);

CREATE TABLE cmt_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES user_info (id),
  operate_time TIMESTAMP NOT NULL,
  comment VARCHAR(255) NOT NULL
);

CREATE TABLE res_statistics (
  res_id INT PRIMARY KEY,
  FOREIGN KEY (res_id) REFERENCES res_info (id),
  click_num INT NOT NULL,
  stu_num INT NOT NULL,
  star_num INT NOT NULL,
  download_num INT NOT NULL,
  rating_num INT NOT NULL,
  difficulty INT DEFAULT NULL,
  rating INT DEFAULT NULL
);

CREATE TABLE exe_statistics (
  exe_id INT PRIMARY KEY, 
  FOREIGN KEY (exe_id) REFERENCES exe_info (id),
  click_num INT NOT NULL,
  stu_num INT NOT NULL,
  collect_num INT NOT NULL,
  answer_num INT NOT NULL,
  error_num INT NOT NULL,
  correct_num INT DEFAULT NULL,
  wrong_num INT DEFAULT NULL,
  answer_easy_if INT DEFAULT NULL,
  difficulty INT DEFAULT NULL
);

CREATE TABLE page_statistics (
  page_id INT NOT NULL, 
  FOREIGN KEY (page_id) REFERENCES page_info (id),
  time_span VARCHAR(50) NOT NULL,
  visit_num INT NOT NULL,
  user_num INT NOT NULL
);