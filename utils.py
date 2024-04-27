import sqlite3


def validate_login(email, password):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute("SELECT password, user_ID FROM Users WHERE email=:email", {"email":email})
    password_found, id = c.fetchone()
    valid = password_found == password
    conn.close()
    return valid, id

def get_post(post_id: int):
    pass

def get_all_posts():
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Posts')
    posts = c.fetchall()
    return posts

def get_comments(post_id: int):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute('SELECT content, user_ID FROM Comments WHERE post_ID=:post_id', {'post_id':post_id})
    comments = c.fetchall()
    usernames = []
    for comment in comments:
        c.execute('SELECT username FROM Users WHERE user_ID=:user_id', {'user_id': comment[1]})
        usernames.append(c.fetchone())
    comments = zip(comments, usernames)
    conn.close()
    return comments

def register_user(username, password, phone, email):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute('INSERT INTO Users (user_Name, password, phone, email) VALUES (:username, :password, :phone, :email)',
               {'username': username, "password": password, "phone": phone, "email":email})
    conn.commit()
    conn.close()

def username_availabe(username):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute("SELECT user_ID FROM Users WHERE user_Name=:username", {'username': username})
    users = c.fetchall()
    conn.close()
    return (len(users) == 0)

def match_passwords(password, conf_password):
    return password == conf_password

def email_availble(email):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute("SELECT user_ID FROM Users WHERE email=:email", {'email': email})
    print('User Added')
    users = c.fetchall()
    conn.close()
    return (len(users) == 0)

def get_user_data(id: int):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE user_ID=:id", {'id': id})
    user = c.fetchone()
    conn.close()
    return user