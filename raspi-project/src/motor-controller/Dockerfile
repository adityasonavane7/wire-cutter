FROM python:3.9-buster

# Update the package list and install required packages
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    python3-setuptools \
    libffi-dev \
    gcc \
    && apt-get clean

RUN pip3 install zmq RPi.GPIO

COPY ./src/stepper_service.py /usr/src/app/stepper_service.py

WORKDIR /usr/src/app

CMD ["python", "stepper_service.py"]