FROM python:3.7-alpine
MAINTAINER Geovany Rodrigues<geovanyscv@gmail.com>

RUN apk update && \
    apk add bash musl-dev zlib-dev jpeg-dev libffi-dev nginx supervisor mariadb-dev gcc linux-headers python3-dev && \
    pip install -U pip setuptools

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN mkdir -p /run/nginx
COPY nginx-app.conf /etc/nginx/conf.d/default.conf
COPY supervisor-app.conf /etc/supervisor-app.conf

# add (the rest of) our code
COPY . /home/docker/code/
WORKDIR /home/docker/code/
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["supervisord", "-n", "--configuration", "/etc/supervisor-app.conf"]
