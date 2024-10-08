import os, gridfs, pika, json

from flask import Flask, request
from flask_pymongo import PyMongo

from auth import validate
from auth_svc import access
from storage import util


server = Flask(__name__)
server.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# mongo interface from the flask app
mongo = PyMongo(server)

# handles size limit in MongoDB (max 16MB)
fs = gridfs.GridFS(mongo.db)

# rabbitmq references RabbitMQ host
rabbitmq_host = os.environ.get("RABBITMQ_HOST")
pika_params = pika.ConnectionParameters(host=rabbitmq_host)
connection = pika.BlockingConnection(pika_params)
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, error = access.login(request)
    if error is None:
        return token
    return error


@server.route("/status", methods=["GET"])
def status():
    return "OK", 200


@server.route("/upload", methods=["POST"])
def upload():
    access, error = validate.token(request)
    if error is not None:
        return error

    access: dict = json.loads(access)

    if access.get("admin"):
        if len(request.files) != 1:
            return "Exactly 1 file required", 400
        
        for filename, file_data in request.files.items():
            file_error = util.upload(file_data, fs, channel, access)
            if file_error:
                return file_error
        
        return "success", 200

    else:
        return "not authorized", 403


@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
    
