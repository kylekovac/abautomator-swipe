# syntax=docker/dockerfile:1
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:367.0.0

RUN apt-get install -y pkg-config
RUN apt-get install -y python3-cairo

WORKDIR /abautomator

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN pip3 install -U pandas
RUN pip3 install --upgrade pandas==1.3.5

WORKDIR /abautomator/app

RUN export FLASK_ENV=development

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]