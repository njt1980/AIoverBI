FROM python:3.10-slim

COPY ./app /app

WORKDIR /app

# RUN apt-get update && apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential default-libmysqlclient-dev && pip install mysqlclient

RUN apt-get update \
    && apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential \
    && pip install mysqlclient

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 7860

ENTRYPOINT [ "python","-u","gradio_chat.py" ]


