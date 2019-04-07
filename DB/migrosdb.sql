DROP DATABASE IF EXISTS Migros;
CREATE DATABASE Migros;

USE Migros;

-- CREATE TABLES
CREATE TABLE user_data (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    loyalty_card_id VARCHARACTER(16) NULL UNIQUE,
    first_name TINYTEXT NOT NULL,
    last_name TINYTEXT NOT NULL,
    email TINYTEXT NOT NULL,
    mobile_phone VARCHARACTER(100) NOT NULL,
    birthday DATE NOT NULL,
    date_joined DATETIME,
    PRIMARY KEY (id),
    UNIQUE (mobile_phone),
    UNIQUE (loyalty_card_id)
);

CREATE TABLE category (
	id int UNSIGNED NOT NULL AUTO_INCREMENT,
	name TINYTEXT NOT NULL,
	PRIMARY KEY (id)
);

-- CREATE TABLE product (
-- 	id int UNSIGNED NOT NULL,
-- 	name TINYTEXT NOT NULL,
-- 	unit_price int UNSIGNED NOT NULL,
-- 	category_id int UNSIGNED NOT NULL,
-- 	point int UNSIGNED NOT NULL,
-- 	PRIMARY KEY (id)
-- );

CREATE TABLE invoice (
	id int UNSIGNED NOT NULL AUTO_INCREMENT,
	user_id int UNSIGNED NOT NULL,
	invoice_date DATETIME,
	total_amount FLOAT UNSIGNED NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE invoice_detail (
	id int UNSIGNED NOT NULL AUTO_INCREMENT,
	invoice_id int UNSIGNED NOT NULL,
	category_id int UNSIGNED NOT NULL,
	amount FLOAT UNSIGNED NOT NULL,
	PRIMARY KEY (id)
);

-- ALTER TABLE product
-- ADD FOREIGN KEY (category_id) REFERENCES category(id);

ALTER TABLE invoice_detail
ADD FOREIGN KEY (invoice_id) REFERENCES invoice(id),
ADD FOREIGN KEY (category_id) REFERENCES category(id);

ALTER TABLE invoice
ADD FOREIGN KEY (user_id) REFERENCES user_data(id);
