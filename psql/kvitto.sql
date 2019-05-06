DROP TABLE IF EXISTS kvitto;

CREATE TABLE kvitto (
    ordernr INTEGER PRIMARY KEY,
    artikelid INTEGER REFERENCES artikel(id),
    producent VARCHAR REFERENCES producent(telnr),
    byer VARCHAR NOT NULL,
    summa FLOAT NOT NULL,
    antal INTEGER NOT NULL,
    datum VARCHAR NOT NULL,
    tid VARCHAR NOT NULL,
    betalt BOOLEAN NOT NULL
);

