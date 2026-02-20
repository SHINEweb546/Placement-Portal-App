from flask import Flask
import sqlite3
app= Flask(__name__)

DB="database.db"

def db_connection():
    conn=sqlite3.connect(DB)
    conn.row_factory=sqlite3.Row
    return conn 
@app.route('/')
def home():
    return "Placement portal is running!"
if __name__=="__main__":
    app.run(debug=True)

    
