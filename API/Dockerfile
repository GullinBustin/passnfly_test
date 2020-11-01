FROM python:3.8.6-alpine3.12

WORKDIR opt
ADD requirements requirements
RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev
RUN apk add --no-cache \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    pip install --no-cache-dir -r requirements/common.txt && \
    apk del \
        libressl-dev \
        musl-dev \
        libffi-dev
ADD source source
WORKDIR source
EXPOSE 5000
CMD python main.py