from flask import Flask,render_template,redirect,url_for,request
from .model import *
from app import app

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login" , methods=["GET","POST"])
def login():
    if request.method == "POST":
        email=request.form.get["email"]
        password=request.form.get["password"]
        user=User.query.filter_by(email = email,password = password).first()
        if user and user.role=="admin":
            return redirect(url_for("admin"))
        elif user and user.role=="user" :
            return redirect(url_for("user"))
        else:
            return render_template("login.html",msg="Invalid credentials !")
    return render_template("login.html")
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        
        email=request.form.get["email"]
        password=request.form.get["password"]
        
        
        user=User.query.filter_by(email = email,password = password).first()
        if user:
            return render_template("register.html",msg="User is already registered !")
        new_user=User(email = email,password = password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html",msg="You are now registered, Go to login and continue !")
    return render_template("register.html")
    
@app.route("/admin")
def admin():
    return "Hii Admin !"

@app.route("/user")
def user():
    return "Hii User !"