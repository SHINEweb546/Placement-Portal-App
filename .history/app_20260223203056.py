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



if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

    
