FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y --no-install-recommends libffi-dev libmagic-dev libmagickwand-dev
RUN apt-get install -y --no-install-recommends libreoffice libreofficekit-dev
RUN apt-get install -y --no-install-recommends python3-dev python3-pip git

RUN apt-get clean && apt-get -y update && apt-get install -y --no-install-recommends locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . /home/docsbox
WORKDIR /home/
RUN pip3 install --upgrade pip
RUN pip3 install -r docsbox/requirements.txt
