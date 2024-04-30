from flask import Flask, render_template, url_for, request, redirect, jsonify
from utils import validate_login, username_availabe, match_passwords, email_availble,\
      register_user, get_user_data, get_all_posts, get_post, get_posts, update_user_data, add_like, get_user_posts, delete_like, new_post_data

app = Flask(__name__)

@app.route('/')
def index():
    top_3 = get_posts(order_by='likes', include_usernames=True)
    RecentPosts = get_posts(order_by='date', num=4)
    Posts = []
    for post, username, comments in zip(RecentPosts['Posts'], RecentPosts['Usernames'], RecentPosts['Comments']):
        Posts.append({'Posts': post, 'Usernames': username, 'Comments':comments})
    return render_template('index.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                            TopPosts=top_3,
                            RecentPosts=Posts)

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


@app.route('/Profile', methods=['POST', 'GET'])
def Profile():
    if not bool(request.cookies.get('LoggedIn')):
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            user = (request.cookies.get('User_id'), request.form['Username'], request.form['Password'], request.form['Phone'], request.form['Email'])
            update_user_data(user)
        else:
            User_Posts = get_user_posts(request.cookies.get('User_id'), include_comments=True)
            Posts = []
            for post, comments in zip(User_Posts['Posts'], User_Posts['Comments']):
                Posts.append({'Posts': post, 'Comments':comments})
            user = get_user_data(request.cookies.get('User_id'))
        return render_template('Profile.html', LoggedIn=bool(request.cookies.get('LoggedIn')),
                                Username="Hello, " + request.cookies.get('Username'),
                                Userdata=user,
                                UserPosts=Posts)

@app.route('/Profile/<Edit>', methods=['GET', 'POST'])
def EditProfile(Edit=None):
    if not bool(request.cookies.get('LoggedIn')):
        return redirect(url_for('index'))
    else:
        user = get_user_data(request.cookies.get('User_id'))
        return render_template('Profile.html',
                                LoggedIn=bool(request.cookies.get('LoggedIn')),
                                Username="Hello, " + request.cookies.get('Username'),
                                Userdata=user, Edit=Edit)

@app.route('/Logout')
def Logout():
    resp = redirect(url_for('index'))
    resp.delete_cookie("Username")
    resp.delete_cookie('LoggedIn')
    resp.delete_cookie('User_id')
    return resp

@app.route('/Posts', methods=['POST', 'GET'])
def Posts():
    if request.method== 'POST':
        if not eval(request.form['Delete'].capitalize()):
            print('Liked')
            add_like(request.cookies.get('User_id'), request.form['post_ID'])
        else:
            print('DisLiked')
            delete_like(request.cookies.get('User_id'), request.form['post_ID'])
        return jsonify(new_post_data(request.form['post_ID']))
    else:
        Posts_dict = get_all_posts(include_likes=True, User_id=request.cookies.get('User_id'))
        Posts = []
        for post, username, comments, Liked in zip(Posts_dict['Posts'], Posts_dict['Usernames'], Posts_dict['Comments'], Posts_dict['Likes']):
            Posts.append({'Posts': post, 'Usernames': username, 'Comments':comments, 'Liked':Liked})

        for post in Posts:
            print(post['Liked'])

        return render_template('postPage.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                                Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                                Posts=Posts)


@app.route('/Posts/<int:Post_id>')
def Post_comments(Post_id=None):
    Post_dict = get_post(Post_id, include_liked=True, User_id=request.cookies.get('User_id'))
    return render_template('postPage.html',
                            LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                            Post=Post_dict,
                            comments=[Post_dict['Comments']],
                            numComments=len(Post_dict['Comments']))

@app.route('/UpdatePosts/<Post_id>', methods=["GET"])
def UpdatePosts(Post_id=None):
    if request.method == 'GET':
        return jsonify(new_post_data(Post_id))
        

@app.route('/AddPost', methods=['POST', 'GET'])
def AddPost():
    if request.method == 'POST':
        imagefile = request.files.get('Poster','')
        print(imagefile)
        title = request.form['Title']
        print(title)
        content = request.form['Content']
        return redirect(url_for('Profile'))
    return render_template('addpost.html', 
                           LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                           Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None)


@app.route('/Post/<int:post_id>')
def Post(post_id=None):
    post = get_post(post_id)
    return render_template('PostTemplate.html', LoggedIn=bool(request.cookies.get('LoggedIn')) if bool(request.cookies.get('LoggedIn')) else None,
                            Username="Hello, " + request.cookies.get('Username') if bool(request.cookies.get('LoggedIn')) else None,
                            Post=post)

if __name__ == "__main__":
    app.run(debug=True)