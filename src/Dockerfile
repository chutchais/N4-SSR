FROM python:3.7.5-alpine

RUN apk update && apk add libpq

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir psycopg2 \
    && apk del --no-cache .build-deps

# Installing and build python module
RUN pip install psycopg2


ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /usr/src/ssr
COPY ./requirements.txt /usr/src/ssr

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#ENTRYPOINT ["python"]
COPY . /usr/src/ssr