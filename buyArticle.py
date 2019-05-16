# coding=utf-8

from flask import request, session
import psycopg2
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def buyArticle():

    antal = request.form['antal']
    articleID = request.form['articleID']

    currentTime = datetime.datetime.now()

    datum = currentTime.strftime('%Y-%m-%d')
    time = currentTime.strftime('%H:%M:%S')

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT MAX(ordernr) FROM kvitto")

    for i in connect:
        if i[0] == None:
            ordernr = 1
        else:
            ordernr = int(i[0] + 1)

    connect.execute("SELECT id, artikel.namn, ordpris, nuvpris, artikel.telnr, email, producent.namn, producentadress.adress FROM artikel JOIN producent ON artikel.telnr = producent.telnr JOIN producentadress ON artikel.telnr = producentadress.telnr WHERE id = %s", (articleID,))

    listWithBuy = []
    for i in connect:
        summaNuv = int(antal) * int(i[3])
        summaOrd = int(antal) * int(i[2])

        listWithBuy.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], summaNuv, summaOrd, antal, datum, time, ordernr])
    
    return listWithBuy

def addToOrders(listWithInfo, byer):

    for i in listWithInfo:
        articleID = i[0]
        producent = i[4]
        datum = i[11]
        tid = i[12]
        summa = i[8]
        antal = i[10]

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

def orders(byer, producent):

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT ordernr, artikelid, producent, byer, summa, kvitto.antal, kvitto.datum, kvitto.tid, producent.namn, email, artikel.namn, adress FROM kvitto JOIN producent ON kvitto.producent = producent.telnr JOIN artikel ON kvitto.artikelid=artikel.id JOIN producentadress ON kvitto.producent = producentadress.telnr WHERE byer = %s ORDER BY ordernr DESC", (byer,))

    listWithOrder = []
    for i in connect:
        listWithOrder.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], producent, i[10], i[11]])

    return listWithOrder

def removeOrder():

    ordernr = int(request.form['ordernr'])

    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("UPDATE kvitto SET betalt = NOT betalt WHERE ordernr = %s", (ordernr,))
    db.commit()

def sendEmail(byer, kvitto):

    for i in kvitto:
        articleID = i[0]
        articleName = i[1]
        # ordPris = i[2]
        # nuvPris = i[3]
        proTelnr = i[4]
        proEmail = i[5]
        proNamn = i[6]
        proAdress = i[7]
        summaNuv = i[8]
        summaOrd = i[9]
        antal = i[10]
        datum = i[11]
        time = i[12]
        orderNr = i[13]
    
    db = psycopg2.connect(dbname="aj1200", user="aj1200", password="gam0gfxz", host="pgserver.mah.se")
    connect = db.cursor()

    connect.execute("SELECT fnamn, enamn FROM konsument WHERE email = %s", (byer,))

    for i in connect:
        byerName = i[0] + " " + i[1]
    
    connect.execute("SELECT namn, nuvpris FROM artikel WHERE expired = False")

    listWithArticles = []
    for i in connect:
        listWithArticles.append([i[0], i[1]])

    me = "FoodtellMAU@gmail.com"
    you = "FoodtellMAU@gmail.com"
    subject = 'Köp från Foodtell'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Något"

    rows = ""
    for i in listWithArticles:
        if i is None:
            rows = rows + """<tr><td style="background: black; color: #ffffff; font-family: courier; font-size: 15px; padding: 10px 40px 10px 40px; text-transform: uppercase; text-align: center;">""" + "Tyvärr finns det inga registrerade erbjudanden" + """</td></tr>"""
        else:
            rows = rows + """<tr><td style="background: black; color: #ffffff; font-family: courier; font-size: 15px; padding: 10px 40px 10px 40px; text-transform: uppercase; text-align: center;">""" + str(i[0]) + """<span style="color: #e85853"> FÖR </span>""" + str(i[1]) + ":-" """</td></tr>"""

    html = """\

    <!DOCTYPE html>

    <html>

        <body style="margin: 70px; font-weight: bolder;">

            <table align="center" border="0" cellspacing="0" cellpadding="0">

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 70px 90px 0 90px; font-size: 40px; line-height: 46px; text-align: center;"> TACK FÖR  <span class="pink" style="color:#e85853;"> DITT KÖP </span> </td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 0 90px 20px 90px; font-size: 40px; line-height: 46px; text-align: center; text-transform: uppercase;"> {} </td>
                </tr>

                <tr>
                    <td style="background: black; color: #e85853; font-family: courier; padding: 0px 90px 50px 90px; font-size: 17px; line-height: 46px; text-align: center;"> DU GÖR GOTT FÖR MILJÖN </td>
                </tr>

                <tr border="0">
                    <td style="background: #e85853;"><img src="https://i.imgur.com/5gF05Vt.jpg"></td>
                </tr>

                <tr border="0">
                    <td style="background: black;"><img src="https://i.imgur.com/C9GDhZp.jpg"></td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 70px 90px 0 90px; font-size: 40px; line-height: 46px; text-align: center;"> DIN <span class="pink" style="color:#e85853;"> BESTÄLLNING </span> </td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 0 90px 0 90px; font-size: 40px; line-height: 36px; text-align: center;"> VISAS NEDAN </td>
                </tr>

                <tr border="0">
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 30px 90px 15px 90px; font-size: 40px; line-height: 46px; text-align: center;"><img style="width: 40px; height: 40px;" src="https://i.imgur.com/XGu85pQ.png"></td>
                </tr>

                <tr>
                    <td style="background: black; color:#ffffff; font-family: courier; font-size:25px; text-align:center; text-transform: uppercase; padding-bottom:16px;"> <span class="pink" style="color:#e85853; border-bottom: 3px solid #e85853;"> Ordernummer {} </span> </td>
                </tr>

                <tr>
                    <td style="background: black; color:#ffffff; font-family: courier; font-size:25px; text-align:center; text-transform: uppercase; padding-bottom:13px;"> artikelid {} </td>
                </tr>

                <tr>
                    <td style="background: black; color:#ffffff; font-family: courier; font-size:25px; text-align:center; text-transform: uppercase; padding-bottom:13px;"> {}x {} </td>
                </tr>

                <tr>
                    <td style="background: black; color:#ffffff; font-family: courier; font-size:25px; text-align:center; text-transform: uppercase; padding-bottom:13px;"> {} </td>
                </tr>

                <tr>
                    <td style="background: black; color:#ffffff; font-family: courier; font-size:25px; text-align:center; text-transform: uppercase; padding-bottom:13px;"> {} </td>
                </tr>

                <tr>
                    <td style="background: black; color:#ffffff; font-family: courier; font-size:25px; text-align:center; text-transform: uppercase; padding-bottom:20px;"> {} </td>
                </tr>

                <tr>
                    <td style="background: black; color:#ffffff; font-family: courier; font-size:25px; text-align:center; text-transform: uppercase; padding-bottom:80px;"> Summa: <span class="pink" style="color:#e85853; border-bottom: 3px solid #e85853;">{}kr </span> </td>
                </tr>

                <tr border="0" style="background: #e85853;">
                    <td><img src="https://i.imgur.com/F39A1d8.jpg"></td>
                </tr>

                <tr border="0" style="background: #e85853;">
                    <td><img style="width: 650px; height: 100px;" src="https://www.colorhexa.com/e85853.png"></td>
                </tr>

                <tr border="0" style="background: black;">
                    <td><img src="https://i.imgur.com/DMLgykX.jpg"></td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 70px 90px 0 90px; font-size: 25px; line-height: 46px; text-transform: uppercase; text-align: center;"> beställningen togs emot </td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 0 90px 0 90px; font-size: 25px; line-height: 46px; text-transform: uppercase; text-align: center;"> av {} den </td>
                </tr>

                <tr>
                    <td style="background: black; color: #e85853; font-family: courier; padding: 0 90px 80px 90px; font-size: 25px; line-height: 46px; text-transform: uppercase; text-align: center;"> <span class="pink" style="color:#e85853; border-bottom: 3px solid #e85853">{}</span> | <span class="pink" style="color:#e85853; border-bottom: 3px solid #e85853">{}</span> </td>
                </tr>

                <tr border="0">
                    <td><img style="margin-bottom: 30px;" src="https://i.imgur.com/QbJbqu2.png"></td>
                </tr>

                <tr>
                    <td style="margin-top: -10px; background: black; color: #ffffff; font-family: courier; padding: 70px 90px 0 90px; font-size: 40px; line-height: 46px; text-transform: uppercase; text-align: center;"> Tillgängliga </td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 0 90px 60px 90px; font-size: 40px; line-height: 46px; text-transform: uppercase; text-align: center;"> <span style="color: #e85853">erbjudanden</span> </td>
                </tr>

                {}

                <tr style="box-sizing: border-box;">
                    <td style="background: black; padding: 35px"> </td>
                </tr>

                <tr border="0" style="background: black;">
                    <td><img style="width: 650px; height: 400px;" src="https://i.imgur.com/dE2JXea.jpg"></td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 70px 90px 0 90px; font-size: 25px; line-height: 46px; text-transform: uppercase; text-align: center;"> Välkommen åter! </td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 0 90px 0 90px; font-size: 25px; line-height: 46px; text-transform: uppercase; text-align: center;"> Besök oss gärna på </td>
                </tr>

                <tr>
                    <td style="background: black; color: #ffffff; font-family: courier; padding: 0 90px 70px 90px; font-size: 25px; line-height: 46px; text-transform: uppercase; text-align: center;"> <a style="color: #e85853;" href="www.foodtell.com"> www.foodtell.com </a> </td>
                </tr>

                <tr border="0">
                    <td><img src="https://i.imgur.com/QbJbqu2.png"></td>
                </tr>

            </table>

        </body>

    </html>

    """.format(byerName, orderNr, articleID, antal, articleName, proNamn, proTelnr, proAdress, summaNuv, proNamn, datum, time, rows)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login("foodtellmau@gmail.com", "Foodtell123")

    server.sendmail(me, you, msg.as_string())
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