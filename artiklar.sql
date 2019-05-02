DROP TABLE IF EXISTS artikel;

CREATE TABLE artikel (
    id INTEGER PRIMARY KEY,
    telnr VARCHAR NOT NULL REFERENCES producent(telnr),
    namn VARCHAR NOT NULL,
    beskrivning VARCHAR NOT NULL,
    datum VARCHAR NOT NULL,
    tid VARCHAR NOT NULL,
    antal INTEGER NOT NULL,
    ordpris FLOAT NOT NULL,
    nuvpris FLOAT NOT NULL
);