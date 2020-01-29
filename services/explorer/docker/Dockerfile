FROM  python:3.8-buster

ARG TZ=America/Los_Angeles 
ARG USER=python-user

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
        echo $TZ > /etc/timezone

RUN apt-get update \
        && apt-get install -y \
        ipython \
        && rm -rf /var/lib/apt/lists/*

RUN wget https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip  \
        && unzip punkt.zip                                      \
        && mkdir -p /usr/local/nltk_data/tokenizers/            \
        && mv punkt /usr/local/nltk_data/tokenizers/            \
        && rm punkt.zip

RUN wget https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/stopwords.zip \
        && unzip stopwords.zip                                  \
        && mkdir -p /usr/local/nltk_data/corpora                \
        && mv stopwords /usr/local/nltk_data/corpora            \
        && rm stopwords.zip

RUN chmod -R 755 /usr/local/nltk_data/

RUN apt-get update && apt-get install -y libxml2-dev            \
        libxslt1-dev antiword unrtf poppler-utils               \
        tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3   \
        sox libjpeg-dev swig libpulse-dev zlib1g-dev            \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY assets/ /

RUN pip install -r requirements.txt

RUN useradd --create-home $USER

