#coding=utf-8

from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
import psycopg2
import article
import encrypt
import logreg

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

def firstLetterUpper(word):
    letters = word[1:]
    firstLetter = word[0].upper()
    return firstLetter + letters

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

    if 'username' in session:
        return redirect(url_for('index'))
    
    else:
        return render_template("register.html")

@app.route("/home", methods=['POST', 'GET'])
def home():

    if 'username' in session:
        username = firstLetterUpper(session['username'].lower())

        return render_template("home.html", username=username)
    
    elif request.method == 'POST':

        if request.form.get('register') == "REGISTER":

            tryRegister = logreg.tryRegister(request.form['username'].lower(), request.form['password'])

            if tryRegister == 'User exist':
                flash('USER ALREADY EXIST', 'error')
                return redirect(url_for('register'))

            else:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
        
        else:

            tryLogin = logreg.tryLogin(request.form['username'].lower(), request.form['password'])

            if tryLogin == 'No username':
                flash('USERNAME DOES NOT EXIST', 'error')
                return redirect(url_for('login'))

            elif tryLogin == 'Logged in':
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            
            else:
                flash('INVALID PASSWORD', 'error')
                return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    
    if 'username' in session:
        return redirect(url_for('home'))
    
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('index'))
    
    else:
        return redirect(url_for('login'))

@app.route("/addarticle", methods=['POST', 'GET'])
def addarticle():

    if 'username' in session:

        if request.method == 'POST':
            article.addArticle()
            return redirect(url_for('articles'))
        
        else:
            return render_template("form.html")
        
    else:
        return redirect(url_for('login'))

@app.route("/articles", methods=['POST', 'GET'])
def articles():

    if 'username' in session:
        article.removeArticle()
        listArticle = article.presentArticle()
        return render_template("artiklar.html", listArticle=listArticle, checkIfEmpty=len(listArticle))
    
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)
def notFound(e):
    return 'This page does not exist', 404

if __name__ == '__main__':
    app.run(debug = True)