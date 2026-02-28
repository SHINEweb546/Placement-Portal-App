from flask import Flask
from Backend.model import db
def setup():
    app= Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    
    print("App has been started")
    return app

app = setup()
from Backend.routes import *



if __name__=="__main__":
    with app.app_context():
        db.create_all()
        admin=User.query.filter_by(email="admin@gmail.com").first()
        if not admin:
            admin=User(
                name="Admin",
                email="admin@gmail.com",
                password="admin123",   
                role="admin",
                is_approved=True

            )
            db.session.add(admin)
            db.session.commit()
            print("Admin created !!")
        else:
            print("Admin is already there")
        app.run(debug=True)


