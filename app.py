#coding=utf-8 

from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
import psycopg2
import article
import encrypt
import log
import reg
import buyArticle
import other

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

app = Flask(__name__)
app.secret_key = "1234abcd"

@app.route("/")
def index():

    if 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:

            return redirect(url_for('home'))
        
        else:

            return redirect(url_for(('notVerified'))) # SKAPA EN HTML FIL
    
    elif 'usernameKonsument' in session:

        return redirect(url_for('home'))

    else:

        return render_template("index.html")

@app.route("/register")
def register():

    if 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:

            return redirect(url_for('home'))
        
        else:

            return redirect(url_for(('notVerified')))
    
    elif 'usernameKonsument' in session:

        return redirect(url_for('home'))
    
    else:
        return render_template("register.html")

@app.route("/home", methods=['POST', 'GET'])
def home():

    producent = None

    if 'usernameKonsument' in session:

        return render_template("home.html", username=session['usernameKonsument'])
    
    elif 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:

            producent = True

            return render_template("home.html", username=session['usernameProducent'], producent=producent)
        
        else:

            return redirect(url_for('notVerified'))
    
    elif request.method == 'POST':

        if request.form.get('registerKonsument') == "REGISTRERA":

            tryRegister = reg.tryRegisterKonsument()

            if tryRegister == 'User exist ON EMAIL AND TELNR':
                flash('USER ALREADY EXIST ON EMAIL AND TELNR', 'error')
                return redirect(url_for('register'))

            elif tryRegister == 'User exist ON EMAIL':
                flash('USER ALREADY EXIST ON EMAIL', 'error')
                return redirect(url_for('register'))

            elif tryRegister == 'User exist ON TELNR':
                flash('USER ALREADY EXIST ON TELNR', 'error')
                return redirect(url_for('register'))

            else:
                session['usernameKonsument'] = tryRegister[1] + " " + tryRegister[2]
                session['emailKonsument'] = tryRegister[0]
                return redirect(url_for('home'))
        
        elif request.form.get('registerProducent') == "REGISTRERA":

            tryRegister = reg.tryRegisterProducent()

            if tryRegister == 'User exist':
                flash('USER ALREADY EXIST ON TELNR', 'error')
                return redirect(url_for('register'))
            else:
                session['telnrProducent'] = tryRegister[0]
                session['emailProducent'] = tryRegister[1]
                session['usernameProducent'] = tryRegister[2]
                return redirect(url_for('home'))

        elif request.form.get('loginKonsument') == "LOGGA IN":

            tryLogin = log.tryLoginKonsument()

            if tryLogin == 'Invalid':
                flash('INVALID DETAILS', 'error')
                return redirect(url_for('login'))

            elif isinstance(tryLogin, (list,)):
                session['usernameKonsument'] = tryLogin[1] + " " + tryLogin[2]
                session['emailKonsument'] = tryLogin[0]
                return redirect(url_for('home'))
            
            else:
                flash('INVALID DETAILS', 'error')
                return redirect(url_for('login'))
            
        else:

            tryLogin = log.tryLoginProducent()

            if tryLogin == 'Invalid':
                flash('INVALID DETAILS', 'error')
                return redirect(url_for('login'))
            
            elif isinstance(tryLogin, (list,)):

                    if len(tryLogin) == 3: # Om det är annan producent än Foodtell
                        session['telnrProducent'] = tryLogin[0]
                        session['emailProducent'] = tryLogin[1]
                        session['usernameProducent'] = tryLogin[2]
                        return redirect(url_for('home'))
                    else:
                        session['telnrFoodtell'] = tryLogin[0]
                        session['emailFoodtell'] = tryLogin[1]
                        session['usernameFoodtell'] = tryLogin[2]
                        return redirect(url_for('foodtell'))
            
            else:
                flash('INVALID DETAILS', 'error')
                return redirect(url_for('login'))
    
    elif 'usernameFoodtell' in session:

        return redirect(url_for('foodtell'))

    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    
    if 'usernameProducent' in session:
        
        if other.verifyProducent(session['telnrProducent']) == True:

            return redirect(url_for('home'))
        
        else:

            return redirect(url_for(('notVerified')))
    
    elif 'usernameKonsument' in session:

        return redirect(url_for('home'))
    
    else:

        return render_template("login.html")

@app.route("/logout")
def logout():

    if 'usernameKonsument' in session:
        session.pop('usernameKonsument', None)
        return redirect(url_for('index'))
    
    elif 'usernameProducent' in session:
        session.pop('usernameProducent', None)
        return redirect(url_for('index'))
    
    elif 'usernameFoodtell' in session:
        session.pop('usernameFoodtell', None)
        return redirect(url_for('index'))
    
    else:
        return redirect(url_for('login'))

@app.route("/addarticle", methods=['POST', 'GET'])
def addarticle():

    if 'usernameKonsument' in session:
        return redirect(url_for('home'))

    elif 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:

            return render_template("form.html")
        
        else:

            return redirect(url_for('notVerified'))
        
    else:
        return redirect(url_for('login'))

@app.route("/articles", methods=['POST', 'GET'])
def articles():

    if 'usernameKonsument' in session or 'usernameProducent' in session:
        article.removeArticleTime()

        if 'usernameProducent' in session:

            if other.verifyProducent(session['telnrProducent']) == True:

                listArticle = article.presentArticleProducent(session['telnrProducent'])
                
                if request.method == 'POST':
                    article.addArticle(session['telnrProducent'])
                    listArticle = article.presentArticleProducent(session['telnrProducent'])
                    return redirect(url_for('articles'))
                else:
                    return render_template("artiklar.html", listArticle=listArticle, checkIfEmpty=len(listArticle), username=session['usernameProducent'])
        
            else:

                return redirect(url_for('notVerified'))
        
        else:
            listArticle = article.presentArticleKonsument()
            return render_template("artiklar.html", listArticle=listArticle, checkIfEmpty=len(listArticle), username=session['usernameKonsument'])
                   
    else:
        return redirect(url_for('login'))

@app.route("/producent")
def producent():

    if 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) != False:

            listWithProducentName = other.getAllProducentName()
            return render_template("producentmain.html", listWithProducentName=listWithProducentName)
        
        else:
            return redirect(url_for('notVerified'))
    
    elif 'usernameKonsument' in session:

        listWithProducentName = other.getAllProducentName()
        return render_template("producentmain.html", listWithProducentName=listWithProducentName)

    else:
        return redirect(url_for('login'))

@app.route("/producent/<telnr>")
def producentname(telnr):

    if 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) != False:

            listWithProducent = other.getProducentInfo(telnr)

            if len(listWithProducent) != 0:
                return render_template("producent.html", listWithProducent=listWithProducent)
            else:
                return redirect(url_for('home'))
        
        else:

            return redirect(url_for('notVerified'))
    
    elif 'usernameKonsument' in session:

        listWithProducent = other.getProducentInfo(telnr)

        if len(listWithProducent) != 0:
            return render_template("producent.html", listWithProducent=listWithProducent)
        else:
            return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))

@app.errorhandler(404)
def notFound(e):
    if 'usernameKonsument' in session or 'usernameProducent' in session or 'usernameFoodtell':
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))

@app.route("/myarticles", methods=['POST', 'GET'])
def myArticles():

    if 'usernameProducent' in session:
        
        if other.verifyProducent(session['telnrProducent']) == True:

            return render_template("producentorders.html")
        
        else:

            return redirect(url_for('notVerified'))
        
    elif 'usernameKonsument' in session:

        return render_template("producentorders.html")
    
    else:
        return redirect(url_for('login'))

@app.route("/myarticles/notexpired", methods=['POST', 'GET'])
def myArticlesNotExpired():

    if 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:
            article.removeArticleTime()

            producentArticles = article.producentArticles(session['telnrProducent'])
            return render_template("myarticles2.html", notExpired=producentArticles[0], empty=len(producentArticles[0]))
        
        else:
            return redirect(url_for('notVerified'))
    
    elif 'usernameKonsument' in session:
        return redirect(url_for('home'))
    
    else:
        return redirect(url_for('login'))

@app.route("/myarticles/expired", methods=['POST', 'GET'])
def myArticlesExpired():

    if 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:
            article.removeArticleTime()

            producentArticles = article.producentArticles(session['telnrProducent'])
            return render_template("myarticles1.html", Expired=producentArticles[1], empty=len(producentArticles[1]))
        
        else:
            return redirect(url_for('notVerified'))
    
    elif 'usernameKonsument' in session:
        return redirect(url_for('home'))
    
    else:
        return redirect(url_for('login'))

@app.route("/myorders", methods=['POST', 'GET']) ######################
def myorders():

    if 'usernameProducent' in session or 'usernameKonsument' in session:

        if request.method == 'POST':

            kvitto = buyArticle.buyArticle()

            if 'usernameKonsument' in session:

                buyArticle.addToOrders(kvitto, session['emailKonsument'])
                buyArticle.sendEmail(session['emailKonsument'], kvitto)
                article.removeArticleAntal()

                return redirect(url_for('myorders'))
            
            else:

                buyArticle.addToOrders(kvitto, session['telnrProducent'])
                buyArticle.sendEmail(session['telnrProducent'], kvitto)
                article.removeArticleAntal()

                return redirect(url_for('myorders'))
        
        else:
            
            if 'usernameProducent' in session:

                if other.verifyProducent(session['telnrProducent']) == True:

                    listWithOrder = buyArticle.orders(session['telnrProducent'], session['usernameProducent'])

                    return render_template("myorders.html", listWithOrder=listWithOrder, empty=len(listWithOrder))
                
                else:

                    return redirect(url_for('notVerified'))
            
        
            else:

                listWithOrder = buyArticle.orders(session['emailKonsument'], session['usernameKonsument'])
                
                return render_template("myorders.html", listWithOrder=listWithOrder)

    else:
        return redirect(url_for('login'))

@app.route("/orders", methods=['POST', 'GET'])
def orders():

    if 'usernameKonsument' in session:
        return redirect(url_for('home'))

    elif 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:

            listWithOrder = buyArticle.producentOrders(session['telnrProducent'])

            return render_template("manageorder.html", listWithOrder=listWithOrder, producent=True, lenOrder=len(listWithOrder))
        
        else:

            return redirect(url_for('notVerified'))
    
    else:
        return redirect(url_for('login'))

@app.route("/removeorder", methods=['POST', 'GET'])
def removeorder():

    if 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == True:

            if request.method == 'POST':

                buyArticle.removeOrder()

                return redirect(url_for('home'))
            
            else:
                return redirect(url_for('home'))
        
        else:
            return redirect(url_for('notVerified'))

    elif 'usernameKonsument' in session:
        return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))

@app.route("/notverified", methods=['GET'])
def notVerified():

    if 'usernameKonsument' in session:

        return redirect(url_for('home'))

    elif 'usernameProducent' in session:

        if other.verifyProducent(session['telnrProducent']) == False:

            return render_template("notVerified.html", username=session['usernameProducent'])
        
        elif other.verifyProducent(session['telnrProducent']) == True:

            return redirect(url_for('home'))
        
        else:

            return redirect(url_for('foodtell'))

    else:

        return redirect(url_for('login'))

@app.route("/foodtell", methods=['GET', 'POST'])
def foodtell():

    if 'usernameFoodtell' in session:

        if request.method == 'GET':

            verified = other.foodtellVerified()
            konsuments = other.allKonsument()
            artiklar = other.allArtiklar()

            return render_template("foodtell.html", username=session['usernameFoodtell'], listVerified=verified[0], listNotVerified=verified[1], konsuments=konsuments, artiklar=artiklar)
        
        else:

            if request.form.get('avverifiera') == "Avverifiera konto":

                other.avverifiera()
            
            elif request.form.get('verifiera') == "Verifiera konto":

                other.verifiera()
            
            elif request.form.get('remove') == "Ta bort konto":

                other.removeKonsument()
            
            elif request.form.get('remove') == "Ta bort / Lägg till":

                other.removeArtikelFoodtell()

            else:
                pass
            
            return redirect(url_for('foodtell'))
        
    else:

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)