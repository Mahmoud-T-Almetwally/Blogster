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
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Posts WHERE post_ID=:post_id', {'post_id':post_id})
    post = c.fetchone()
    c.execute('SELECT user_Name FROM Users WHERE user_ID=:user_id', {'user_id':post[-1]})
    username = c.fetchone()
    post = (post, username)
    conn.close()
    return post

def get_posts(order_by=None, num=3, include_usernames=False, month=None, year=None):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()

    months = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }

    sql = 'SELECT * FROM Posts '

    if month and year:
        date = year + '-' + month[month] + '-00'
        endDate = year + '-' + str(int(month[month]) + 1) + '-00'
        sql += 'WHERE date >= ' + date + " AND date < " + endDate

    if order_by:
        sql += 'ORDER BY ' + order_by

    c.execute(sql)
    top = c.fetchmany(num)

    if include_usernames:
        usernames = []
        comments = []
        for post in top:
            c.execute('SELECT user_Name FROM Users WHERE user_ID=:user_id', {'user_id': post[-1]})
            usernames.append(c.fetchone())
            c.execute('SELECT comment_ID FROM Comments WHERE post_ID=:post_id', {'post_id': post[0]})
            comments.append(len(c.fetchall()))
        top = zip(top, usernames)
        top = zip(top, comments)

    return top

def get_all_posts():
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Posts')
    posts = c.fetchall()
    usernames = []
    comments = []
    print(posts)
    for post in posts:
        c.execute('SELECT user_Name FROM Users WHERE user_ID=:user_id', {'user_id': post[-1]})
        usernames.append(c.fetchone())
        c.execute('SELECT comment_ID FROM Comments WHERE post_ID=:post_id', {'post_id': post[0]})
        comments.append(len(c.fetchall()))
    posts = zip(posts, usernames)
    posts = zip(posts, comments)
    conn.close()
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

def update_user_data(Userdata):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute('UPDATE Users SET user_Name=:new_name, password=:new_password, phone=:new_phone, email=:new_email WHERE user_ID=:user_id',
             {'new_name':Userdata[1], 'new_password':Userdata[2], 'new_phone':Userdata[3], 'new_email':Userdata[4], 'user_id':Userdata[0]})
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