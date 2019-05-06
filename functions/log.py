# coding=utf-8

from flask import request
import psycopg2
import encrypt
import other

def tryLoginKonsument():

    email = request.form['emailKonsument'].lower()
    password = request.form['passwordKonsument']

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT email, fnamn, enamn, password FROM konsument WHERE email = %s", (email,))

    varEmail = None

    for i in connect:
        varEmail = i[0]
        decryptedPassword = encrypt.checkEncryptedPassword(password, i[3])
        
    if varEmail == None:
        return 'Invalid'
                
    elif varEmail == email and decryptedPassword is True:
        listMessage = other.sessionsForKonsument(email)
        return listMessage
                
    else:
        return 'Invalid'

def tryLoginProducent():

    telnr = request.form['numberProducent']
    password = request.form['passwordProducent']

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT telnr, namn, password FROM producent WHERE telnr = %s", (telnr,))

    varTelnr = None

    for i in connect:
        namn = i[1]
        varTelnr = i[0]
        decryptedPassword = encrypt.checkEncryptedPassword(password, i[2])
    
    if varTelnr == None:
        return 'Invalid'
                
    elif varTelnr == telnr and decryptedPassword is True:
        listMessage = other.sessionsForProducent(telnr)
        return listMessage
                
    else:
        return 'Invalid'