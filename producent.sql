DROP TABLE IF EXISTS producent;

CREATE TABLE producent (
    telnr VARCHAR PRIMARY KEY,
    email VARCHAR NOT NULL,
    namn VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

DROP TABLE IF EXISTS producentAdress;

CREATE TABLE producentAdress (
    telnr VARCHAR PRIMARY KEY REFERENCES producent(telnr),
    adress VARCHAR NOT NULL
);