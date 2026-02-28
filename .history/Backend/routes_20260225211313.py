from flask import Flask,render_template,redirect,url_for
from .model import *
from app import app

@app.route("/")
def home():
    return render_template("home.html")
@app.route