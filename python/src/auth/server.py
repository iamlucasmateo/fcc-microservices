import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
for var in ["HOST", "USER", "PASSWORD", "DB", "PORT"]:
    name = f"MYSQL_{var}"
    server.config[name] = os.environ.get(name)

@server.route("/login", methods=["POST"])
def loging():
    # the request object contains data for simple authorization
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    # check DB for user and pass
    cur = mysql.connection.cursor()
    values = (auth.username,)
    query = "SELECT email, password FROM user WHERE email=%s"
    res = cur.execute(query, values)
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    return "invalid credentials", 401
        