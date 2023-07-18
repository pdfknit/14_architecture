
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS visitors;
CREATE TABLE visitors (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));
INSERT INTO visitors (id, name) VALUES (1, 'Ivan Ivanov');
INSERT INTO visitors (id, name) VALUES (2, 'Alisa Vetrova');
INSERT INTO visitors (id, name) VALUES (3, 'Inna Rostova');
INSERT INTO visitors (id, name) VALUES (4, 'Fedor Petrov');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
