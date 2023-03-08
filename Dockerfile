FROM python:3.8 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/code/src/"
ADD . /code
WORKDIR /code

COPY . .

RUN pip install --no-cache-dir pipenv && pipenv install --dev --system --deploy
