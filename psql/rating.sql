DROP TABLE IF EXISTS rating;

CREATE TABLE rating (
    email VARCHAR,
    telnr VARCHAR,
    rating INTEGER,
    FOREIGN KEY(email) REFERENCES konsument(email),
    FOREIGN KEY(telnr) REFERENCES producent(telnr),
)