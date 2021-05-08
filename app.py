# sample-web-app/app.py
from flask import Flask 
  
app = Flask(__name__)
messages = []
  
@app.route("/") 
def home_view(): 
        return "<h1>Welcome to My website!</h1>"