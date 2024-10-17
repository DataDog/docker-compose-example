FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

# Set DD tags
ENV DD_SERVICE web
ENV DD_ENV sandbox
ENV DD_VERSION 1.0
