FROM python:3.7

COPY . /opt
WORKDIR /opt

RUN pip3 install -r requirements.txt

EXPOSE 5000/tcp

ENTRYPOINT ./manage.py runserver --host 0.0.0.0