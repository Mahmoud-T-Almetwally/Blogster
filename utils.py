import sqlite3


def validate_login(email, password):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE email=:email", {"email":email})
    user = c.fetchone()
    valid = user[2] == password
    conn.close()
    return valid, user

def get_post(post_id: int):
    pass

def get_posts(post_id: list, num: int):
    pass

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
    c.execute("SELECT * FROM Users WHERE user_Name=:username", {'username': username})
    users = c.fetchall()
    conn.close()
    return (len(users) == 0)

def match_passwords(password, conf_password):
    return password == conf_password

def email_availble(email):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE email=:email", {'email': email})
    print('User Added')
    users = c.fetchall()
    conn.close()
    return (len(users) == 0)