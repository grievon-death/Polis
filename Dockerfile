FROM python:3.10-alpine

RUN apk update
RUN apk upgrade
RUN apk update && apk add --virtual build-deps gcc bash make python3

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

