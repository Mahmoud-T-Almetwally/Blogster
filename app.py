from flask import Flask, render_template, url_for, request, redirect
from utils import validate_login, username_availabe, match_passwords, email_availble, register_user, get_user_data, get_comments, get_all_posts, get_post, get_posts

app = Flask(__name__)

@app.route('/')
def index():
    top_3 = get_posts(order_by='likes', include_usernames=True)
    RecentPosts = get_posts(order_by='date', num=4)
    return render_template('index.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                            TopPosts=top_3,
                            RecentPosts=RecentPosts)

@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == "POST":
        valid, id = validate_login(request.form['email'].lower(), request.form['password'])
        if valid:
            user = get_user_data(id)
            resp = redirect(url_for('index'))
            resp.set_cookie('LoggedIn', 'True')
            resp.set_cookie('Username', user[1])
            resp.set_cookie('User_id', str(user[0]))
            return resp
    return render_template('login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if not username_availabe(request.form['username']):
            return render_template('signup.html', user_not_avail=True)
            
        if not match_passwords(request.form['password'], request.form['conf_password']):
            return render_template('signup.html', passwords_dont_match=True)
        
        if not email_availble(request.form['email'].lower()):
            return render_template('signup.html', email_taken = True)
        
        register_user(request.form['username'], request.form['password'], request.form['number'], request.form['email'].lower())
        _, user = validate_login(request.form['email'].lower(), request.form['password'])
        resp = redirect(url_for('index'))
        resp.set_cookie('LoggedIn', 'True')
        resp.set_cookie('Username', user[1])
        resp.set_cookie('User_id', str(user[0]))
        return resp
    else:
        return render_template('signup.html')
        
    

@app.route('/about')
def about():
    return render_template('about.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None)


@app.route('/Profile')
def Profile():
    if not bool(request.cookies.get('LoggedIn')):
        return redirect(url_for('index'))
    else:
        user = get_user_data(request.cookies.get('User_id'))
        return render_template('Profile.html', LoggedIn=bool(request.cookies.get('LoggedIn')), Username="Hello, " + request.cookies.get('Username'), Userdata=user)

@app.route('/Logout')
def Logout():
    resp = redirect(url_for('index'))
    resp.delete_cookie("Username")
    resp.delete_cookie('LoggedIn')
    resp.delete_cookie('User_id')
    return resp

@app.route('/Posts')
def Posts():
    Posts = get_all_posts()
    return render_template('postPage.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                            Posts=Posts)

@app.route('/Posts/<Post_id>')
def Post_comments(Post_id=None):
    return render_template('postPage.html',
                            LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                            Post=get_post(Post_id),
                            comments=get_comments(request.args.get('Post_id')),
                            numComments=len(list(get_comments(request.args.get('Post_id')))))

@app.route('/Post/<int:post_id>')
def Post(post_id=None):
    post = get_post(post_id)
    return render_template('PostTemplate.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                            Post=post)

if __name__ == "__main__":
    app.run(debug=True)