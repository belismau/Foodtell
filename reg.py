# coding=utf-8

from flask import request
import psycopg2
import encrypt
import other

def tryRegisterKonsument():
    
    email = request.form['emailKonsument'].lower()
    fnamn = other.firstLetterUpper(request.form['fnamnKonsument'])
    enamn = other.firstLetterUpper(request.form['enamnKonsument'])
    telnr = request.form['telnrKonsument']
    password = request.form['passwordKonsument']

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT konsumenttelnr.email FROM konsumenttelnr WHERE konsumenttelnr.email = %s", (email,))

    varEmail = False

    for i in connect:
        if email == i[0]:
            varEmail = True
    
    connect.execute("SELECT telnr FROM konsumenttelnr WHERE telnr = %s", (telnr,))

    varTelnr = False

    for i in connect:
        if int(telnr) == int(i[0]):
            varTelnr = True

    if varEmail == True and varTelnr == True:
        return 'User exist ON EMAIL AND TELNR'
    elif varEmail == True:
        return 'User exist ON EMAIL'
    elif varTelnr == True:
        return 'User exist ON TELNR'
    else:
        pass
    
    if varEmail == False and varTelnr == False:

        encryptedPassword = encrypt.encryptPassword(password)

        connect.execute("INSERT INTO konsument VALUES(%s, %s, %s, %s)", (email, fnamn, enamn, encryptedPassword))
        db.commit()

        connect.execute("INSERT INTO konsumenttelnr VALUES(%s, %s)", (email, telnr))
        db.commit()

        listMessage = other.sessionsForKonsument(email)

        return listMessage

def tryRegisterProducent():

    email = request.form['emailProducent'].lower()
    username = request.form['usernameProducent']
    adress = other.firstLetterUpper(request.form['adressProducent'])
    telnr = request.form['nummerProducent']
    password = request.form['passwordProducent']

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT telnr from producent")

    varTelnr = False
    
    for i in connect:
        if telnr == i[0]:
            varTelnr = True
            return 'User exist'
            
    if varTelnr is False:
        encryptedPassword = encrypt.encryptPassword(password)
                
        connect.execute("INSERT INTO producent VALUES(%s, %s, %s, %s)", (telnr, email, username, encryptedPassword))
        db.commit()

        connect.execute("INSERT INTO producentadress VALUES(%s, %s)", (telnr, adress))
        db.commit()

        listMessage = other.sessionsForProducent(telnr)

        return listMessage