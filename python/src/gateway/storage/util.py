import json

import pika


def upload(file_data, fs, channel, access):
    """Uploads video and posts a message in the channel."""
    try:
        file_id = fs.put(file_data)
    except Exception as error:
        return "Internal server error uploading file", 500
    
    message = {
        "video_file_id": str(file_id),
        "mp3_file_id": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="", # this uses the default exchange
            routing_key="video", # the default exchange will pass this to the correct queue
            body=json.dumps(message),
            properties=pika.BasicProperties(
                # if the node fails or crashes, the queue and the messages are persisted
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            )
        )
    except:
        fs.delete(file_id)
        return "Internal server error posting message to queue", 500

