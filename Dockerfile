# FROM python:3.9-buster
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:367.0.0

RUN gcloud config set project citizen-ops-21adfa65

RUN apt-get install -y pkg-config
RUN apt-get install -y python3-cairo

WORKDIR /abautomator

# Base Python packages
# RUN pip install --upgrade pip
# RUN pip install --upgrade google-cloud-bigquery-storage
# RUN pip install pytest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD bash