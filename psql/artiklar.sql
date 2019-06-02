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
    category VARCHAR NOT NULL
);

INSERT INTO artikel VALUES
(0,'0709876543','Hamburgare','En hamburgare','2019-06-2','19:11',10,100,50,FALSE,'Amerikanskt'),
(1,'0709876543','Hamburgare','En hamburgare','2019-06-2','19:11',10,100,50,FALSE,'Italienskt'),
(2,'0709876543','Hamburgare','En hamburgare','2019-06-2','19:11',10,100,50,FALSE,'Orientaliskt'),
(3,'0709876543','Hamburgare','En hamburgare','2019-06-2','19:11',10,100,50,FALSE,'Asiatiskt'),
(4,'0709876543','Hamburgare','En hamburgare','2019-06-2','19:11',10,100,50,FALSE,'Kafé');
