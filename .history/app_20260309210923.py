from flask import Flask
from Backend.model import db
from Backend.routes import *
def create_applications():
    app= Flask(__name__)
    app.secret_key="placementportal345"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    
    print("Placement Portal is started")
    return app

app = create_applications()




if __name__=="__main__":
    with app.app_context():
        db.create_all()
        admin_present=User.query.filter_by(email="admin@gmail.com").first()
        if not admin_present:
            default_admin=User(
                name="Admin",
                email="admin@gmail.com",
                password="admin123",   
                role="admin",
                is_approved=True

            )
            db.session.add(default_admin)
            db.session.commit()
            print("Admin created successfully!!")
        else:
            print("Admin account already available")
        app.run(debug=True)


