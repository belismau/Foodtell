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

def sessionsForFoodtell(telnr):
    
    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT * FROM producent WHERE producent.telnr = %s", (telnr,))

    listWithSession = []
    for i in connect:
        listWithSession.append(i[0])
        listWithSession.append(i[1])
        listWithSession.append(i[2])
        listWithSession.append("Foodtell")

    return listWithSession

def getProducentInfo(telnr):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT producent.telnr, email, namn, producentadress.adress, verified FROM producent JOIN producentadress on producent.telnr = producentadress.telnr WHERE producent.telnr = %s", (telnr,))

    listWithProducent = []
    
    for i in connect:
        if i[4] == True:
            listWithProducent.append([i[0], i[1], i[2], i[3]])
    
    return listWithProducent

def getAllProducentName():

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT namn, telnr, verified FROM producent")

    listWithProducentName = []
    
    for i in connect:
        if i[2] == True:
            listWithProducentName.append([i[0], i[1]])
    
    return listWithProducentName

def verifyProducent(producent):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT verified FROM producent WHERE telnr = %s", (producent,))

    for i in connect:
        if i[0] == True:
            return True
        elif i[0] == False:
            return False
        else:
            return 'Foodtell'

def foodtellVerified():

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT producent.telnr, email, namn, adress, verified FROM producent JOIN producentadress ON producent.telnr = producentadress.telnr")

    listVerified = []
    listNotVerified = []

    for i in connect:
        if i[4] == True:
            listVerified.append([i[0], i[1], i[2]])
        elif i[4] == False:
            listNotVerified.append([i[0], i[1], i[2]])
        else:
            pass
    
    listAll = []
    listAll.append(listVerified)
    listAll.append(listNotVerified)

    return listAll

def avverifiera():

    telnr = request.form['telnr']

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("UPDATE producent SET verified = False WHERE telnr = %s", (telnr,))
    db.commit()

def verifiera():

    telnr = request.form['telnr']

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("UPDATE producent SET verified = True WHERE telnr = %s", (telnr,))
    db.commit()




