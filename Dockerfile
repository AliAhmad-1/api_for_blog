FROM python:alpine3.19

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /code

COPY requirements.txt .
RUN python -m pip install -r requirements.txt


COPY . .