import os, gridfs, pika, json

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from pymongo import errors as pymongo_errors

from auth import validate
from auth_svc import access
from storage import util
from app_logger import get_logger

logger = get_logger(__name__)

load_dotenv()

server = Flask(__name__)
server.config["MONGO_URI"] = os.environ.get("MONGO_URI")
server.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 * 10 # 160 MB

# mongo interface from the flask app
mongo = PyMongo(server)
mongo.db = mongo.cx[os.environ.get("MONGO_VIDEOS_DB")]
# handles size limit in MongoDB (max 16MB)
fs = gridfs.GridFS(mongo.db)

# rabbitmq references RabbitMQ host
rabbitmq_host = os.environ.get("RABBITMQ_HOST")
pika_params = pika.ConnectionParameters(host=rabbitmq_host)
connection = pika.BlockingConnection(pika_params)
channel = connection.channel()
# channel = ""

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


@server.route("/check_db_auth", methods=["GET"])
def check_db_auth():
    try:
        # Use the 'admin' database for the ismaster command
        server_status = mongo.db.command("ismaster")

        # Try to list all collection names in the current database
        collection_names = mongo.db.list_collection_names()

        return jsonify(is_master=server_status, is_authorized=True, collections=collection_names), 200
    except pymongo_errors.OperationFailure as exc:
        logger.debug(f"Unauthorized access to the database: {repr(exc)}")
        # If listing the collections fails, the credentials are not authorized
        return jsonify(is_master=False, is_authorized=False), 403


if __name__ == "__main__":
    SERVER_HOST = os.environ.get("SERVER_HOST")
    SERVER_PORT = os.environ.get("SERVER_PORT")
    server.run(host=SERVER_HOST, port=SERVER_PORT)
    
