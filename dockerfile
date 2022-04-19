FROM ubuntu:latest

RUN apt-get update

# Set timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install tzdata
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

# get files
RUN apt install -y software-properties-common

RUN apt install -y python3
RUN apt install -y python3-pip

RUN apt install -y firefox
RUN apt install -y firefox-geckodriver

# RUN apt install -y cron

# Debug
RUN apt install -y nano

# Project
COPY main.py /scraper/
RUN chmod +x /scraper/
RUN chmod +x /scraper/main.py

RUN pip3 install selenium

WORKDIR /scraper/

# CMD python3 /scraper/main.py

# docker build -t ig_scr1 .
# docker save -o ./ig_scr1.tar ig_scr1
# docker run -it -v data:/scraper/data ig_scr1:latest