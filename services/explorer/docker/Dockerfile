FROM  python:3.8-buster

ARG TZ=America/Los_Angeles
ARG USER=python-user

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
        echo $TZ > /etc/timezone

RUN apt-get update \
        && apt-get install -y \
        ipython \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY assets/ /

RUN pip install -r requirements.txt

RUN useradd --create-home $USER

