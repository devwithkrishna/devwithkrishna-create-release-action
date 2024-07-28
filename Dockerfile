# Using official python image as base image
FROM python:3.11-slim-bullseye

# Setting a label
LABEL authors="githubofkrishnadhas"

# Configuring workdir
WORKDIR /app

# Copies your code file from your action repository to the container
COPY . /app/

# Install pipenv
RUN chmod +x entrypoint.sh &&  apt-get update -y && pip install --upgrade pip && pip install poetry

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/app/entrypoint.sh"]