import pika, sys, os
from pymongo import MongoClient
import gridfs
import to_mp3


MONGO_URI = os.environ.get("MONGO_URI")
MONGO_PORT = int(os.environ.get("MONGO_PORT"))
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_VIDEO_QUEUE = os.environ.get("RABBITMQ_VIDEO_QUEUE")


def main():
  client = MongoClient(MONGO_URI)
  db_videos = client.video
  db_mp3s = client.mp3s
  fs_videos = gridfs.GridFS(db_videos)
  fs_mp3s = gridfs.GridFS(db_mp3s)
  
  connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST)
  )
  channel = connection.channel()

  def _on_video_message_callback(channel, method, properties, body):
    err = to_mp3.start(body, fs_videos, fs_mp3s, channel)
    if err:
      # nack = negative acknowledgement - message will not be removed from the queue
      channel.basic_nack(delivery_tag=method.delivery_tag)
    else:
      channel.basic_ack(delivery_tag=method.delivery_tag)
    

  channel.basic_consume(
    queue=RABBITMQ_VIDEO_QUEUE,
    on_message_callback=_on_video_message_callback
  )

  print("Waiting for messages, to exit hit Ctrl+C")

  channel.start_consuming()

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("Interrupted")
    # shutdown gracefully
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)




