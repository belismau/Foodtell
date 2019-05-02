DROP TABLE IF EXISTS konsument;

CREATE TABLE konsument (
    email VARCHAR PRIMARY KEY,
    fnamn VARCHAR NOT NULL,
    enamn VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

DROP TABLE IF EXISTS konsumentTelnr;

CREATE TABLE konsumentTelnr (
    email VARCHAR REFERENCES users(email),
    telnr VARCHAR NOT NULL
);