# coding=utf-8

import psycopg2
import encrypt

def tryLogin(username, email, password):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT username, email, password FROM users WHERE username = %s", (username,))

    usernameInput = None
    emailInput = None

    for i in connect:
        usernameInput = i[0]
        emailInput = i[1]
        decryptedPassword = encrypt.checkEncryptedPassword(password, i[2])
    
    if usernameInput is None or emailInput is None:
        return 'Invalid'
            
    elif usernameInput == username and emailInput == email and decryptedPassword is True:
        return 'Logged in'
            
    else:
        return 'Invalid'

def tryRegister(username, email, password):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT username, email FROM users")

    usrnrEmail = False
    for i in connect:
        if username == i[0] or email == i[1]:
            usrnrEmail = True
            return 'User exist'
            
    if usrnrEmail is False:
        listWithID = []
        connect.execute("SELECT id FROM users")
        for i in connect:
            listWithID.append(i[0])
        db.commit()

        if len(listWithID) == 0:
            currentID = 1
        else:
            currentID = listWithID[len(listWithID)-1] + 1
                
        encryptedPassword = encrypt.encryptPassword(password)
                
        connect.execute("INSERT INTO users VALUES(%s, %s, %s, %s)", (currentID, username, email, encryptedPassword))
        db.commit()

        return 'Registered'