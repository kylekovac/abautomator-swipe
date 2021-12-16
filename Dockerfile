FROM python:3.9-buster

WORKDIR /transformations

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

COPY . .

CMD bash