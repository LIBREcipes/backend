FROM python:3.7.7-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . ./

CMD ["gunicorn", "--bind", "0.0.0.0:80", "librecipes.wsgi"]
