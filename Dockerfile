FROM python:3.7

COPY . /opt
WORKDIR /opt

RUN pip3 install -r requirements.txt
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
RUN chmod +x cloud_sql_proxy

ENV GOOGLE_APPLICATION_CREDENTIALS="/opt/service_accout_key.json"

EXPOSE 8080/tcp

ENTRYPOINT ./manage.py runserver --host 0.0.0.0 --port 8080
