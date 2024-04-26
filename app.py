from flask import Flask, render_template, url_for, request, redirect
from utils import validate_login

app = Flask(__name__)

@app.route('/')
def index():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('index.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST": 
        valid, user = validate_login(request.form['email'], request.form['password'])
        if valid:
            resp = redirect(url_for('index'))
            resp.set_cookie('LoggedIn', 'True')
            resp.set_cookie('Username', user[1])
            return resp
    return render_template('login.html')

@app.route('/contact')
def contact():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('contact.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('contact.html')

@app.route('/signup')
def signup():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('signup.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('signup.html')

@app.route('/about')
def about():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('about.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('about.html')

@app.route('/Post/<int:post_id>')
def get_post(post_id):
    if bool(request.cookies.get('LoggedIn')):
        return render_template('Post.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('Post.html')

@app.route('/Profile')
def Profile():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('Profile.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('Profile.html')

@app.route('/Logout')
def Logout():
    resp = redirect(url_for('index'))
    resp.delete_cookie("Username")
    resp.delete_cookie('LoggedIn')
    return resp

if __name__ == "__main__":
    app.run(debug=True)