FROM python:3.12-slim-bookworm

COPY app/requirements.txt ./
RUN pip install -r requirements.txt

COPY app/ ./

RUN ls -lah

ENV WORKERS "2"
