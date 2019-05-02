#coding=utf-8

from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
import psycopg2
import article
import encrypt
import log
import reg
import other

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

app = Flask(__name__)
app.secret_key = "1234abcd"

@app.route("/")
def index():

    if 'username' in session:
        return redirect(url_for('home'))

    else:
        return render_template("index.html")

@app.route("/register")
def register():

    if 'usernameKonsument' in session:
        return redirect(url_for('index'))
    
    else:
        return render_template("register.html")

@app.route("/home", methods=['POST', 'GET'])
def home():

    addArticle = None

    if 'usernameKonsument' in session:

        return render_template("home.html", username=session['usernameKonsument'])
    
    elif 'usernameProducent' in session:

        addArticle = True

        return render_template("home.html", username=session['usernameProducent'], addArticle=addArticle)
    
    elif request.method == 'POST':

        if request.form.get('registerKonsument') == "REGISTER":

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
        
        elif request.form.get('registerProducent') == "REGISTER":

            tryRegister = reg.tryRegisterProducent()

            if tryRegister == 'User exist':
                flash('USER ALREADY EXIST ON TELNR', 'error')
                return redirect(url_for('register'))
            else:
                session['telnrProducent'] = tryRegister[0]
                session['emailProducent'] = tryRegister[1]
                session['usernameProducent'] = tryRegister[2]
                return redirect(url_for('home'))

        elif request.form.get('loginKonsument') == "LOGIN":

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
                session['telnrProducent'] = tryLogin[0]
                session['emailProducent'] = tryLogin[1]
                session['usernameProducent'] = tryLogin[2]
                return redirect(url_for('home'))
            
            else:
                flash('INVALID DETAILS', 'error')
                return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    
    if 'usernameKonsument' in session:
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
    
    else:
        return redirect(url_for('login'))

@app.route("/addarticle", methods=['POST', 'GET'])
def addarticle():

    if 'usernameKonsument' in session:
        return redirect(url_for('home'))

    elif 'usernameProducent' in session:
        return render_template("form.html")
        
    else:
        return redirect(url_for('login'))

@app.route("/articles", methods=['POST', 'GET'])
def articles():

    if 'usernameKonsument' in session or 'usernameProducent' in session:
        article.removeArticleTime()
        listArticle = article.presentArticle()

        if 'usernameKonsument' in session:
            return render_template("artiklar.html", listArticle=listArticle, checkIfEmpty=len(listArticle), username=session['usernameKonsument'])
        
        else:
            if request.method == 'POST':
                article.addArticle(session['telnrProducent'])
                
            return render_template("artiklar.html", listArticle=listArticle, checkIfEmpty=len(listArticle), username=session['usernameProducent'])    
    else:
        return redirect(url_for('login'))

@app.route("/articles/<articleID>", methods=['POST', 'GET'])
def order(articleID):

    if 'usernameProducent' in session or 'usernameKonsument' in session:

        listWithInfo = article.infoAboutArticle(articleID)

        if len(listWithInfo) != 0:
            return render_template("artikelinfo.html", listWithInfo=listWithInfo)
        else:
            return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))

@app.route("/producent")
def producent():

    if 'usernameProducent' in session or 'usernameKonsument' in session:

        listWithProducentName = other.getAllProducentName()

        return render_template("producentmain.html", listWithProducentName=listWithProducentName)

    else:
        return redirect(url_for('login'))

@app.route("/producent/<telnr>")
def producentname(telnr):

    if 'usernameProducent' in session or 'usernameKonsument' in session:

        listWithProducent = other.getProducentInfo(telnr)

        if len(listWithProducent) != 0:
            return render_template("producent.html", listWithProducent=listWithProducent)
        else:
            return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))
        

@app.errorhandler(404)
def notFound(e):
    if 'usernameKonsument' in session or 'usernameProducent' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True)