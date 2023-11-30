FROM python:3.8
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev pkg-config

# Set the working directory in the container
WORKDIR /django

# Copy requirements.txt and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
