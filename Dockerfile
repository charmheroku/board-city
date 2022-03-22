# pull official base image
FROM python:3.8
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
COPY Pipfile Pipfile.lock /usr/src/app/
RUN pip install pipenv && pipenv install --system
# Copy project
COPY . /usr/src/app/