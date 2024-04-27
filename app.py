from flask import Flask, render_template, url_for, request, redirect
from utils import validate_login, username_availabe, match_passwords, email_availble, register_user

app = Flask(__name__)

@app.route('/')
def index():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('index.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == "POST": 
        valid, user = validate_login(request.form['email'], request.form['password'])
        if valid:
            resp = redirect(url_for('index'))
            resp.set_cookie('LoggedIn', 'True')
            resp.set_cookie('Username', user[1])
            resp.set_cookie('User_id', user[0])
            return resp
    return render_template('login.html')

@app.route('/contact')
def contact():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('contact.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if not username_availabe(request.form['username']):
            return render_template('signup.html', user_not_avail=True)
            
        if not match_passwords(request.form['password'], request.form['conf_password']):
            return render_template('signup.html', passwords_dont_match=True)
        
        if not email_availble(request.form['email']):
            return render_template('signup.html', email_taken = True)
        
        register_user(request.form['username'], request.form['password'], request.form['number'], request.form['email'])
        _, user = validate_login(request.form['email'], request.form['password'])
        resp = redirect(url_for('index'))
        resp.set_cookie('LoggedIn', 'True')
        resp.set_cookie('Username', user[1])
        resp.set_cookie('User_id', str(user[0]))
        return resp
    else:
        return render_template('signup.html')
        
    

@app.route('/about')
def about():
    if bool(request.cookies.get('LoggedIn')):
        return render_template('about.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('about.html')


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
    resp.delete_cookie('User_id')
    return resp

@app.route('/Post/<int:post_id>')
def get_post(post_id):

    if bool(request.cookies.get('LoggedIn')):
        return render_template('Post.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'))
    else:
        return render_template('Post.html')

if __name__ == "__main__":
    app.run(debug=True)