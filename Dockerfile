FROM python:3

LABEL MAINTAINER="Don Dayley <example@domain.com>"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/
ADD . /var/www/
RUN apt-get update 
RUN apt install -y libmariadb3 libmariadb-dev
RUN pip install -r requirements.txt

#RUN sudo apt-get install python3.6-dev
#RUN sudo apt install uwsgi uwsgi-plugin-python3
#RUN sudo apt install uwsgi uwsgi-plugin-python3
RUN addgroup -gid $GROUP_ID www
RUN adduser -gid $GROUP_ID www --disabled-password --gecos ""

USER www

COPY . .
EXPOSE 5001

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5001", "wsgi"]

#CMD [ "uwsgi", "--ini", "app.ini" ]