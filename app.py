from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contact')
def login():
    return render_template('contact.html')

@app.route('/signup')
def login():
    return render_template('signup.html')

@app.route('/about')
def login():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)