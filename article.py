# coding=utf-8

from flask import request, session
import psycopg2
import datetime

def removeArticleAntal():

    antal = request.form['antal']
    articleID = request.form['id']

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT id, antal FROM artikel WHERE id = %s", (articleID,))

    resultat = connect.fetchall()

    for i in resultat:

        if i[1] == int(antal):
            connect.execute("DELETE FROM artikel WHERE id = %s", (articleID,))
            db.commit()
        else:
            newAntal = i[1] - int(antal)
            connect.execute("UPDATE artikel SET antal = %s WHERE id = %s", (newAntal, articleID))
            db.commit()

def removeArticleTime():
    
    # Kopplar upp mig till databasen

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    # Nuvarande tid

    currentTime = datetime.datetime.now()

    # Nuvarande datum

    currentDate = datetime.datetime(currentTime.year, currentTime.month, currentTime.day)
 
    connect.execute("SELECT tid, datum, id FROM artikel")

    # Så att FLERA artiklar kan tas bort från databasen

    resultat = connect.fetchall()

    # Ta reda på om artiklar ska tas bort med hänsyn till nuvarande tid

    for i in resultat:
        
        # Artiklens datum från db uppdelat i år, månad och dag

        year = int(i[1][0:4])
        month = int(i[1][5:7])
        day = int(i[1][8:10])

        # Artiklens tid från db uppdelat i timmar och minuter
    
        articleHour = int(i[0][0:2])
        articleMin = int(i[0][3:5])

        # Artikelns datum i formatet enligt datetime

        articleDate = datetime.datetime(year, month, day)

        # Om artikelns datum < nuvarande datum

        if articleDate < currentDate:
            connect.execute("DELETE FROM artikel WHERE id = %s", (i[2],))
            db.commit()
        
        # Om artikelns datum = nuvarande datum

        elif articleDate == currentDate:

            # Om artikelns timvisare < nuvarande timvisaren
        
            if articleHour < currentTime.hour:
                connect.execute("DELETE FROM artikel WHERE id = %s", (i[2],))
                db.commit()
            
            # Om artikelns timvisare = nuvarande timvisaren

            elif articleHour == currentTime.hour:

                # Om artikelns minutvisare är mindre eller lika med nuvarande minutvisaren
            
                if articleMin <= currentTime.minute:
                    connect.execute("DELETE FROM artikel WHERE id = %s", (i[2],))
                    db.commit()
                
                # Tar INTE bort om artikelns datum = nuvarande datum...
                # ... om artikelns timvisare = nuvarande timvisaren...
                # ... men artikelns minutvisare > nuvarande minutvisaren

                else:
                    pass

            # Tar INTE bort artikeln om artikelns datum = nuvarande datum...
            # ... men artikelns timvisare > nuvarande timvisaren

            else:
                pass
            
        # Tar INTE bort artikeln om artikelns datum > nuvarande datum

        else:
            pass

def presentArticle():

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    listArticle = []
    connect.execute("SELECT id, artikel.namn, beskrivning, datum, tid, antal, ordpris, nuvpris, producent.namn FROM artikel join producent on artikel.telnr=producent.telnr")
    for i in connect:
        listArticle.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]])
    db.commit()

    return listArticle

def addArticle(telnr):

    namn = request.form['namn']
    beskrivning = request.form['beskrivning']
    tid = request.form['time']
    datum = request.form['date']
    antal = request.form['antal']
    ordpris = request.form['ordinariepris']
    nuvpris = request.form['nuvarandepris']

    # Kopplar upp mig till databasen

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    # Lägger till alla ID i en lista

    listWithID = []
    connect.execute("SELECT id FROM artikel")
    for i in connect:
        listWithID.append(i[0])
    db.commit()

    # Tar det sista ID:et i tabellen och ökar det med 1

    if len(listWithID) == 0:
        currentID = 1
    else:
        currentID = listWithID[len(listWithID)-1] + 1

    # Lägger till informationen i databasen

    connect.execute("INSERT INTO artikel VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (currentID, telnr, namn, beskrivning, datum, tid, antal, ordpris, nuvpris))
    db.commit()

def infoAboutArticle(articleID):
    
    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT artikel.id, producent.telnr, producent.email, producent.namn  FROM artikel JOIN producent ON artikel.telnr=producent.telnr  WHERE artikel.id = %s", (articleID,))

    listWithInfo = []

    for i in connect:
        listWithInfo.append(i[0])
        listWithInfo.append(i[1])
        listWithInfo.append(i[2])
        listWithInfo.append(i[3])

    return listWithInfo