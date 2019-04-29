DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

INSERT INTO users VALUES(1, 'Test1', 'test@hotmail.com', 'willbeencrypted');