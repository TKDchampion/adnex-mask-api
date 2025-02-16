FROM python:3.9

WORKDIR /code

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

RUN chmod +x /code/start.sh

CMD ["/code/start.sh"]
