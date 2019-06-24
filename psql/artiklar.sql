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
    nuvpris FLOAT NOT NULL,
    expired BOOLEAN,
    category VARCHAR NOT NULL,
    rating INTEGER NOT NULL
);

INSERT INTO artikel VALUES
(0,'0709876543','Hamburgare','En hamburgare','2019-08-2','19:11',10,100,50,FALSE,'Amerikanskt',0),
(1,'0709876543','Hamburgare','En hamburgare','2019-08-2','19:11',10,100,50,FALSE,'Italienskt',0),
(2,'0709876543','Hamburgare','En hamburgare','2019-08-2','19:11',10,100,50,FALSE,'Orientaliskt',0),
(3,'0709876543','Hamburgare','En hamburgare','2019-08-2','19:11',10,100,50,FALSE,'Asiatiskt',0),
(4,'0709876543','Hamburgare','En hamburgare','2019-08-2','19:11',10,100,50,FALSE,'Kafé',0);
