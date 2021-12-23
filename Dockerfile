# FROM python:3.9-buster
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:367.0.0

WORKDIR /abautomator

# Base Python packages
RUN pip install --upgrade pip
RUN pip install --upgrade google-cloud-bigquery-storage

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

# COPY . .

CMD bash