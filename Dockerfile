FROM python:3.10.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONNOBYTECODE=1

WORKDIR /code/

COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv && pipenv install --system

COPY . /code/


