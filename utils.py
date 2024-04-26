import sqlite3


def validate_login(email, password):
    conn = sqlite3.connect('DB/blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE email=:email", {"email":email})
    user = c.fetchone()
    valid = user[2] == password
    conn.close()
    return valid, user
