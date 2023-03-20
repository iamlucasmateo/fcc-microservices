import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)

environment = {
    "MYSQL_HOST": "localhost",
    "MYSQL_USER": "fcc",
    "MYSQL_PASSWORD": "Admin_fcc123",
    "MYSQL_DB": "fcc_micros",
    "MYSQL_PORT": 3306,
    "JWT_SECRET": "my_jwt_secret"
}

# config
for key, value in environment.items():
    os.environ[key] = str(value)
    server.config[key] = value

mysql = MySQL(server)

@server.route("/login", methods=["POST"])
def login():
    # the request object contains data for simple authorization
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    # check DB for user and pass
    cur = mysql.connection.cursor()
    values = (auth.username,)
    query = "SELECT email, password, isAdmin FROM user WHERE email=%s"
    res = cur.execute(query, values)
    if res > 0:
        user_row = cur.fetchone()
        email, password, is_admin = user_row
        is_admin = bool(is_admin)

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), is_admin)
    
    return "invalid credentials", 401

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials", 401
    auth_type, token = encoded_jwt.split(" ")
    try:
        decoded = jwt.decode(
            token,
            os.environ.get("JWT_SECRET"),
            algorithms=["HS256"]
        )
    except:
        return "not authorized", 403
    
    return decoded, 200



def createJWT(username: str, secret: str, isAdmin: bool):
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    expiration = now + datetime.timedelta(days=1)
    userData = {
        "username": username,
        "exp": expiration,
        "iat": now,
        "admin": isAdmin
    }
    return jwt.encode(userData,
        secret,
        algorithm="HS256"
    )

def validateJWT():
    pass

if __name__ == "__main__":
    # this works for Docker networks. Flask app will be listening to all IPs within the Docker
    # container that hosts them. The IP asigned to the Docker container is subject to change, 
    # and the same container can have different addresses in different networks that it is part of.
    # so, by listening on all IP adresses of the Docker container, the app will always get the requests directed at it.
    all_ips = "0.0.0.0"
    server.run(host=all_ips, port=5000)