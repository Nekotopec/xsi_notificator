FROM python:3.8-alpine

RUN mkdir /code
WORKDIR /code
RUN mkdir /server
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk update \
    && apk add --no-cache gcc git python3-dev yaml-dev musl-dev linux-headers \
    libc-dev  rsync zsh \
    findutils wget util-linux grep libxml2-dev libxslt-dev \
    &&  pip3 install --upgrade pip
RUN pip install -U setuptools pip
RUN pip install aiohttp
RUN pip install --global-option='--with-libyaml' pyyaml
ENV PYTHONPATH=/code
COPY ./server/subscribe.py /code/server/subscribe.py
COPY ./server/config.py /code/server/config.py
COPY ./settings.yaml /code