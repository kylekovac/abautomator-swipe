# syntax=docker/dockerfile:1
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:367.0.0

RUN apt-get install -y pkg-config
RUN apt-get install -y python3-cairo

WORKDIR /abautomator

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD cd app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]