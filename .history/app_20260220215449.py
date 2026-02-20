from flask import Flask
# from Backend.model import db

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URL"]


@app.route('/')
def home():
    return "Placement portal is running!"
if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

    
