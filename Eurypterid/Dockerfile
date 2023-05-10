# Dockerfile

FROM python:3.9-buster

# install nginx
RUN apt-get update && apt-get install vim tesseract-ocr tesseract-ocr-eng tesseract-ocr-tam tesseract-ocr-mal tesseract-ocr-tel tesseract-ocr-hin ffmpeg libsm6 libxext6 -y --no-install-recommends
# COPY nginx.default /etc/nginx/sites-available/default
# RUN true
# RUN ln -sf /dev/stdout /var/log/nginx/access.log \
#    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies

ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8000  
# start server  
CMD python manage.py runserver 0.0.0.0:8000