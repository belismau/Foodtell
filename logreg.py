# coding=utf-8

import psycopg2
import encrypt

def tryLogin(username, password):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT username, password FROM users WHERE username = %s", (username,))

    usernameInput = None

    for i in connect:
        usernameInput = i[0]
        decryptedPassword = encrypt.checkEncryptedPassword(password, i[1])
            
    if usernameInput is None:
        return 'No username'
            
    elif usernameInput == username and decryptedPassword is True:
        return 'Logged in'
            
    else:
        return 'Invalid'

def tryRegister(username, password):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT username FROM users")

    usrnr = False
    for i in connect:
        if username == i[0]:
            usrnr = True
            return 'User exist'
            
    if usrnr is False:
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
                
        connect.execute("INSERT INTO users VALUES(%s, %s, %s)", (currentID, username, encryptedPassword))
        db.commit()

        return 'Registered'