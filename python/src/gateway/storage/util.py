import json
import os

import pika

from app_logger import get_logger

logger = get_logger(__name__)


def upload(file_data, fs, channel, access, filename):
    """Uploads video and posts a message in the channel."""
    try:
        file_id = fs.put(file_data)
    except Exception as error:
        logger.debug(f"Error uploading file {filename}: {error}")
        return "Internal server error uploading file", 500
    
    message = {
        "video_file_id": str(file_id),
        "mp3_file_id": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="", # this uses the default exchange
            routing_key=os.environ.get("VIDEO_ROUTING_KEY"), # the default exchange will pass this to the correct queue
            body=json.dumps(message),
            properties=pika.BasicProperties(
                # if the node fails or crashes, the queue and the messages are persisted
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            )
        )
    except:
        fs.delete(file_id)
        return "Internal server error posting message to queue", 500

