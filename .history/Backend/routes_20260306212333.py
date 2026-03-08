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
            return redirect(url_for("admin_dashboard"))
        elif user and user.role=="student" :
            return redirect(url_for("student_dashboard"))
        elif user and user.role=="company" :
            if user.is_approved:
                return redirect(url_for("company_daashboard"))
            else:
                return render_template("login.html", msg="Company not approved by admin yet")
        return render_template("login.html" , msg="Invalid details")   
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        
        
        user=User.query.filter_by(name=name, email = email,password = password).first()
        if user:
            return render_template("register.html",msg="User is already registered !")
        new_user=User(name=name,email = email,password = password, role="student")
        db.session.add(new_user)
        db.session.commit()
        return render_template("register.html",msg="You are now registered, Go to login and continue !")
    return render_template("register.html")
    
@app.route("/admin")
def admin_dashboard():
    users=User.query.all()
    jobs=Job.query.all()
    company=User.query.filter_by(role="company").all()
    return render_template("admin/admin_dashboard.html",
                           users=users,jobs=jobs,company=company)

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
@app.route("/student")
def student_dashboard():
    
    jobs_list=Job.query.all()
    return render_template("student/student_dashboard.html",jobs_list=jobs_list)


    
@app.route("/student/jobs")
def view_jobs():
    jobs = Job.query.filter_by(status="open").all()
    return render_template("student/student_job.html", jobs=jobs)
@app.route("/user/apply/<int:job_id>")
def apply_job(job_id):
    application = Application(
        student_id=1,   # TEMP (will be session-based later)
        job_id=job_id,
        status="applied"
    )

    db.session.add(application)
    db.session.commit()
    return redirect(url_for("student_dashboard"))

    
@app.route("/student/applications")
def my_applications():
    applications = Application.query.filter_by(student_id=1).all()
    return render_template(
        "student/student_application.html",
        applications=applications
    )
@app.route("/make_company", methods=["GET","POST"])
def make_company():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        company = User(
            name=name,
            email=email,
            password=password,
            role="company"
        )

        db.session.add(company)
        db.session.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template("admin/make_company.html")
@app.route("/company_dashboard")
def company_dashboard():
    jobs_list=Job.query.all()
    return render_template("company/company_daashboard.html")

@app.route("/approve_company/<int:id>")
def approve_company(id):
    company = User.query.get(id)

    company.is_approved = True
    db.session.commit()

    return redirect(url_for("admin_dashboard"))