from flask import Flask,render_template,redirect,url_for,request
from .model import *
from app import app

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login" , methods=["GET","POST"])
def login():
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
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
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        
        
        user=User.query.filter_by(name=name, email = email,password = password).first()
        if user:
            return render_template("register.html",msg="User is already registered !")
        new_user=User(name=name,email = email,password = password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("register.html",msg="You are now registered, Go to login and continue !")
    return render_template("register.html")
    
@app.route("/admin")
def admin_dashboard():
    users=User.query.all()
    jobs=Job.query.all()
    return render_template("admin/admin_dashboard.html",
                           users=users,jobs=jobs)

@app.route("/admin/approve/<int:user_id>")
def approve_user(user_id):
    user = User.query.get(user_id)
    user.is_approved = True
    db.session.commit()
    return redirect(url_for("admin_dashboard"))
@app.route("/admin/delete/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))
@app.route("/admin/job/add", methods=["GET", "POST"])
def add_job():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        job = Job(
            title=title,
            description=description,
            status="open",
            company_id=1  # TEMP admin/company id
        )

        db.session.add(job)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/add_job.html")
@app.route("/admin/job/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    job = Job.query.get(job_id)

    if request.method == "POST":
        job.title = request.form.get("title")
        job.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

    return render_template("admin/edit_job.html", job=job)
@app.route("/admin/job/delete/<int:job_id>")
def delete_job(job_id):
    job = Job.query.get(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))
@app.route("/user")
def user():
    return "Hii User !"