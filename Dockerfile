FROM arm64v8/python

RUN apt-get update
RUN apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libevent-dev \
    wget \
    gcc \
    git


RUN mkdir -p /metastax
WORKDIR /metastax

ADD . /metastax
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

