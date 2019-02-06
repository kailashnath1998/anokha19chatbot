FROM python:3.6.8-alpine3.8

RUN apk update && apk add --no-cache supervisor

RUN mkdir -p /etc/supervisor.d

COPY supervisord.conf /etc/supervisord.conf

COPY . /app

WORKDIR /app

RUN pip install -r requirments.txt

EXPOSE 6789

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
