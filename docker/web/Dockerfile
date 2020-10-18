FROM python:3.8-alpine

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk update \
    && apk add --no-cache gcc python3-dev yaml-dev musl-dev linux-headers \
    libc-dev  rsync zsh \
    findutils wget util-linux grep libxml2-dev libxslt-dev \
    &&  pip3 install --upgrade pip
RUN pip install -U setuptools pip
RUN pip install -r requirements.txt
RUN pip install --global-option='--with-libyaml' pyyaml
COPY ./server/ /code/server
COPY ./settings.yaml /code
COPY sleep.py /code
ENV PYTHONPATH=/code