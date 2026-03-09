from flask import Flask,render_template,redirect,url_for,request,session
from .model import *
from app import app


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email, password=password).first()

        if not user:
            return render_template("login.html", msg="Invalid email or password")

        session["user_id"] = user.id

        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))

        elif user.role == "student":
            return redirect(url_for("student_dashboard"))

        elif user.role == "company":
            if user.is_approved:
                return redirect(url_for("company_dashboard"))
            else:
                return render_template("login.html", msg="Company not approved by admin yet")

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
@app.route("/student_dashboard")
def student_dashboard():
    
    jobs_list=Job.query.all()
    return render_template("student/student_dashboard.html",jobs_list=jobs_list)


    
@app.route("/student/student_job")
def view_jobs():
    jobs = Job.query.filter_by(status="open").all()
    return render_template("student/student_job.html", jobs=jobs)
@app.route("/student/apply/<int:job_id>")
def apply_job(job_id):
    student_id=session.get("user_id")
    application = Application(
        student_id=student_id,   
        job_id=job_id,
        status="applied"
    )

    db.session.add(application)
    db.session.commit()
    return redirect(url_for("student_dashboard"))

    
@app.route("/student/student_applications")
def my_applications():
    applications = Application.query.filter_by(student_id=student_id).all()
    student_id=session.get("user_id")
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
    return render_template("company/company_dashboard.html",jobs_list=jobs_list)

@app.route("/approve_company/<int:id>")
def approve_company(id):
    company = User.query.get(id)

    company.is_approved = True
    db.session.commit()

    return redirect(url_for("admin_dashboard"))
@app.route("/company/add_job_company", methods=["GET","POST"])
def add_job_company():
    if request.method== "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        new_job = Job(title=title, description=description,status="open",company_id=1)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for("company_dashboard"))

    return render_template("company/add_job.html")
@app.route("/edit_job_company/<int:id>", methods=["GET","POST"])
def edit_job_company(id):

    job = Job.query.get(id)

    if request.method == "POST":

        job.title = request.form.get("title")
        job.description = request.form.get("description")

        db.session.commit()

        return redirect(url_for("company_dashboard"))

    return render_template("company/edit_job.html", job=job)
@app.route("/delete_job_company/<int:id>")
def delete_job_company(id):

    job = Job.query.get(id)

    db.session.delete(job)
    db.session.commit()

    return redirect(url_for("company_dashboard"))
@app.route("/admin/applications")
def admin_applications():

    applications = Application.query.all()

    return render_template(
        "admin/admin_applications.html",
        applications=applications
    )
@app.route("/approve_application/<int:id>")
def approve_application(id):

    application = Application.query.get(id)

    application.status = "Approved"

    db.session.commit()

    return redirect(url_for("admin_applications"))
@app.route("/reject_application/<int:id>")
def reject_application(id):

    application = Application.query.get(id)

    application.status = "Rejected"

    db.session.commit()

    return redirect(url_for("admin_applications"))
@app.route("/create_drive", methods=["GET","POST"])
def create_drive():

    if request.method == "POST":

        title = request.form.get("title")
        company = request.form.get("company")
        date = request.form.get("date")
        description = request.form.get("description")

        drive = PlacementDrive(
            title=title,
            company_name=company,
            date=date,
            description=description
        )

        db.session.add(drive)
        db.session.commit()

        return redirect(url_for("admin_dashboard"))

    return render_template("admin/create_drive.html")
@app.route("/placement_drives")
def placement_drives():

    drives = PlacementDrive.query.all()

    return render_template(
        "student/placement_drives.html",
        drives=drives
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))