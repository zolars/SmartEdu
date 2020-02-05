CREATE DATABASE smartedu CHARACTER SET utf8 COLLATE utf8_general_ci;
USE smartedu;

CREATE TABLE user_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  reg_ip VARCHAR(16) NOT NULL,
  reg_time TIMESTAMP NOT NULL,
  birthday TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  mobile VARCHAR(12) DEFAULT NULL,
  province VARCHAR(255) DEFAULT NULL,
  city VARCHAR(255) DEFAULT NULL, 
  gender BOOLEAN DEFAULT NULL, /* 0 for female, 1 for male */
  customer_name VARCHAR(255) DEFAULT NULL,
  student_id VARCHAR(11) NOT NULL,
  email VARCHAR(255) DEFAULT NULL,
  signature VARCHAR(255) DEFAULT NULL,
  id_active BOOLEAN DEFAULT NULL, /* 0 for deactive, 1 for active */
  id_alive BOOLEAN DEFAULT 1 /* 0 for pause, 1 for alive */
);

CREATE TABLE admin_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE chapter_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE res_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  context VARCHAR(255) UNIQUE NOT NULL, /* include cover.jpg and context */
  chapter_id INT NOT NULL,
  FOREIGN KEY (chapter_id) REFERENCES chapter_info (id),
  difficulty INT NOT NULL, /* 1 for easy, 2 for normal, 3 for difficult */
  enter_user INT NOT NULL, 
  FOREIGN KEY (enter_user) REFERENCES admin_info (id),
  enter_time TIMESTAMP DEFAULT now(),
  title VARCHAR(255) NOT NULL,
  type INT NOT NULL, /* 1 for video, 2 for doc, 3 for other */
  rating INT NOT NULL,
  description VARCHAR(255) DEFAULT NULL,
  duration INT DEFAULT NULL
);

CREATE TABLE exe_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  context VARCHAR(255) UNIQUE NOT NULL, /* include prob.jpg and ans.jpg */
  chapter_id INT NOT NULL,
  FOREIGN KEY (chapter_id) REFERENCES chapter_info (id),
  difficulty INT NOT NULL, /* 1 for easy, 2 for normal, 3 for difficult */
  enter_user INT NOT NULL,
  FOREIGN KEY (enter_user) REFERENCES admin_info (id),
  enter_time TIMESTAMP DEFAULT now()
);

CREATE TABLE hw_info (
  id INT PRIMARY KEY AUTO_INCREMENT,
  context VARCHAR(255) UNIQUE NOT NULL, /* include cover.jpg and context */
  chapter_id INT NOT NULL,
  FOREIGN KEY (chapter_id) REFERENCES chapter_info (id),
  difficulty INT NOT NULL, /* 1 for easy, 2 for normal, 3 for difficult */
  enter_user INT NOT NULL,
  FOREIGN KEY (enter_user) REFERENCES admin_info (id),
  enter_time TIMESTAMP DEFAULT now(),
  week VARCHAR(50) NOT NULL
);


CREATE TABLE user_auth_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  user_ip VARCHAR(16) NOT NULL,
  operation INT NOT NULL, /* 0 for logout, 1 for login */
  time TIMESTAMP NOT NULL,
  os VARCHAR(255) DEFAULT NULL,
  browser VARCHAR(255) DEFAULT NULL,
  resolution VARCHAR(255) DEFAULT NULL /* 屏幕分辨率 */
);

CREATE TABLE res_history (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT DEFAULT NULL, 
  FOREIGN KEY (user_id) REFERENCES user_info (id),
  user_ip VARCHAR(16) NOT NULL,
  res_id INT NOT NULL, 
  FOREIGN KEY (res_id) REFERENCES res_info (id),
  operation INT NOT NULL, /* 0 for popupping from collection; 1 for adding into collection; 2 for download; 3 for rating */
  time TIMESTAMP NOT NULL,
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
  user_id INT DEFAULT NULL, 
  FOREIGN KEY (user_id) REFERENCES user_info (id),
  user_ip VARCHAR(16) NOT NULL,
  pagepath VARCHAR(255) NOT NULL,
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
  pagepath VARCHAR(255) NOT NULL,
  time_span VARCHAR(50) NOT NULL,
  visit_num INT NOT NULL,
  user_num INT NOT NULL
);