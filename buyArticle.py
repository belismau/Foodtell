# coding=utf-8

from flask import request, session
import psycopg2
import datetime
import smtplib

def buyArticle():

    antal = request.form['antal']
    articleID = request.form['articleID']

    currentTime = datetime.datetime.now()

    datum = currentTime.strftime('%Y-%m-%d')
    time = currentTime.strftime('%H:%M:%S')

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT id, artikel.namn, ordpris, nuvpris, artikel.telnr, email, producent.namn FROM artikel JOIN producent ON artikel.telnr = producent.telnr WHERE id = %s", (articleID,))

    listWithBuy = []
    for i in connect:
        summaNuv = int(antal) * int(i[3])
        summaOrd = int(antal) * int(i[2])

        listWithBuy.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], summaNuv, summaOrd, antal, datum, time])
    
    return listWithBuy

def addToOrders(listWithInfo, byer):

    for i in listWithInfo:
        articleID = i[0]
        producent = i[4]
        datum = i[10]
        tid = i[11]
        summa = i[7]
        antal = i[9]

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT MAX(ordernr) FROM kvitto")

    for i in connect:
        if i[0] == None:
            ordernr = 1
        else:
            ordernr = int(i[0] + 1)

    connect.execute("INSERT INTO kvitto VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (ordernr, articleID, producent, byer, summa, antal, datum, tid, False))
    db.commit()

def orders(byer, name):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT ordernr, artikelid, producent, byer, summa, antal, datum, tid, producent.namn, email FROM kvitto JOIN producent ON kvitto.producent = producent.telnr WHERE byer = %s", (byer,))

    listWithOrder = []
    for i in connect:
        listWithOrder.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], name])

    return listWithOrder

def removeOrder():

    ordernr = int(request.form['ordernr'])

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("UPDATE kvitto SET betalt = NOT betalt WHERE ordernr = %s", (ordernr,))
    db.commit()

def sendEmail(konsument, producent):

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("foodtellmau@gmail.com", "Foodtell123")
    msg = "Tack för din beställning, {}!\nHär kommer ett kvitto på ditt köp från {}.".format(konsument, producent)
    server.sendmail(
        "foodtellmau@gmail.com", 
        "foodtellmau@gmail.com", 
        msg)
    server.quit()

def producentOrders(producent):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    # FÖR DE KONSUMENTER SOM BESTÄLLT

    connect.execute("SELECT ordernr, artikelid, artikel.namn, fnamn, enamn, byer, konsumenttelnr.telnr, summa, kvitto.antal, kvitto.datum, kvitto.tid, betalt FROM kvitto JOIN konsument ON byer=konsument.email JOIN artikel ON artikelid=artikel.id JOIN konsumenttelnr ON byer=konsumenttelnr.email WHERE producent = %s", (producent,))

    listWithOrder = []
    for i in connect:

        ordernr = i[0]
        artikelID = i[1]
        artikelNamn = i[2]
        namnKonsument = i[3] + " " + i[4]
        email = i[5]
        telnr = i[6]
        summa = i[7]
        antal = i[8]
        datum = i[9]
        tid = i[10]
        betalt = i[11]

        if betalt == False:
            listWithOrder.append([ordernr, artikelID, artikelNamn, namnKonsument, email, telnr, summa, antal, datum, tid, False])
        else:
            listWithOrder.append([ordernr, artikelID, artikelNamn, namnKonsument, email, telnr, summa, antal, datum, tid, True])

    # FÖR DE PRODUCENTER SOM BESTÄLLT

    connect.execute("SELECT ordernr, artikelid, artikel.namn, producent.namn, byer, producent.email, summa, kvitto.antal, kvitto.datum, kvitto.tid, betalt FROM kvitto JOIN artikel ON artikelid=artikel.id JOIN producent ON byer=producent.telnr WHERE producent = %s", (producent,))
    
    for i in connect:

        ordernr = i[0]
        artikelID = i[1]
        artikelNamn = i[2]
        namnProducent = i[3]
        email = i[5]
        telnr = i[4]
        summa = i[6]
        antal = i[7]
        datum = i[8]
        tid = i[9]
        betalt = i[10]

        if betalt == False:
            listWithOrder.append([ordernr, artikelID, artikelNamn, namnProducent, email, telnr, summa, antal, datum, tid, False])
        else:
            listWithOrder.append([ordernr, artikelID, artikelNamn, namnProducent, email, telnr, summa, antal, datum, tid, True])

    return listWithOrder