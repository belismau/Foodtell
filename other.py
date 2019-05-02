# coding=utf-8

from flask import request
import psycopg2
import encrypt

def firstLetterUpper(word):
    letters = word[1:].lower()
    firstLetter = word[0].upper()
    return firstLetter + letters

def sessionsForProducent(telnr):
    
    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT * FROM producent WHERE producent.telnr = %s", (telnr,))

    listWithSession = []
    for i in connect:
        listWithSession.append(i[0])
        listWithSession.append(i[1])
        listWithSession.append(i[2])

    return listWithSession

def sessionsForKonsument(email):
    
    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT * FROM konsument WHERE konsument.email = %s", (email,))

    listWithSession = []
    for i in connect:
        listWithSession.append(i[0])
        listWithSession.append(i[1])
        listWithSession.append(i[2])

    return listWithSession

def getProducentInfo(telnr):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT producent.telnr, email, namn, producentadress.adress FROM producent JOIN producentadress on producent.telnr = producentadress.telnr WHERE producent.telnr = %s", (telnr,))

    listWithProducent = []
    
    for i in connect:
        listWithProducent.append([i[0], i[1], i[2], i[3]])
    
    return listWithProducent

def getAllProducentName():

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT namn, telnr FROM producent")

    listWithProducentName = []
    
    for i in connect:
        listWithProducentName.append([i[0], i[1]])
    
    return listWithProducentName
