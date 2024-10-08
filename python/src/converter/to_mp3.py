import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message_json, fs_videos, fs_mp3s, channel):
  message = json.loads(message_json)
  # empty temp file
  tf = tempfile.NamedTemporaryFile()
  # video contents
  out = fs_videos.get(ObjectId(message["video_fid"])).read()
  # add video contents to empty file
  tf.write(out.read())
  # create audio form temp video file
  # tf.name will have the path to the temp file
  audio = moviepy.editor.VideoFileClip(tf.name).audio
  # this will delete the temp file
  tf.close()

  # write audio to temp file
  tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
  audio.write_audiofile(tf_path)

  # save file to Mongo
  f = open(tf_path, "rb")
  data = f.read()
  fid = fs_mp3s.put(data)
  f.close()
  os.remove(tf_path)

  message["mp3_fid"] = str(fid)

  try:
    channel.basic_publish(
      exchange="",
      routing_key=os.environ.get("RABBITMQ_MP3_QUEUE"),
      body=json.dumps(message),
      properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
    )
  except Exception as e:
    # Remove file from MongoDB if we can't publish
    fs_mp3s.delete(fid)
    return "Failed to publish message"

