FROM python:3.9-slim

RUN pip install RPi.GPIO

COPY ./src/stepper_service.py /usr/src/app/stepper_service.py

WORKDIR /usr/src/app

CMD ["python", "stepper_service.py"]