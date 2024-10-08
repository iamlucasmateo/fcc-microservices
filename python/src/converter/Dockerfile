# Base image ("file system snapshot")
FROM python:3.10-slim-bullseye

# no-install flags makes this layer lighter
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential ffmpeg \
    && pip install --no-cache-dir --upgrade pip

# create working directory
WORKDIR /app
# if requirements change, the image has to be rebuilt from here
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
# if one of our source files changes (other than requirements.txt), Docker build rebuild from here 
COPY . /app

CMD ["python3", "consumer.py"]