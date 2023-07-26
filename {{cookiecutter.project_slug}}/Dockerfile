FROM python:3.10.8-slim-bullseye
WORKDIR /app
RUN apt-get update \
      && apt-get -y install apt-utils default-postgres-client build-essential \
      libffi-dev
COPY . /app
COPY certs/ca-certificate.crt /etc/certs/
RUN pip install sqlalchemy gevent
RUN pip install -r requirements/prod.txt
RUN chmod +x /app/entrypoint.sh \
      && chmod +x /app/celery.sh
CMD [ "/app/entrypoint.sh" ]