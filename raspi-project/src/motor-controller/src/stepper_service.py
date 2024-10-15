import RPi.GPIO as GPIO
import time
from confluent_kafka import Consumer, KafkaError

class StepperMotorController:
    def __init__(self, step_pin, dir_pin, enable_pin=None):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        if self.enable_pin is not None:
            GPIO.setup(self.enable_pin, GPIO.OUT)
            GPIO.output(self.enable_pin, GPIO.LOW)  # Enable the motor

    def set_direction(self, direction):
        if direction == '+':
            GPIO.output(self.dir_pin, GPIO.HIGH)  # Clockwise
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)   # Counterclockwise

    def send_pulse(self, num_pulses):
        for _ in range(abs(num_pulses)):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(0.001)

    def move_motor(self, direction, num_pulses):
        self.set_direction(direction)
        self.send_pulse(num_pulses)

    def cleanup(self):
        GPIO.cleanup()

def kafka_consumer(motor):
    # Configure Kafka consumer
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'stepper-group',
        'auto.offset.reset': 'earliest'
    })
    
    consumer.subscribe(['stepper-motor-commands'])

    try:
        while True:
            msg = consumer.poll(1.0)  # Poll for messages

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    break

            # Process the message
            command = msg.value().decode('utf-8')
            print(f"Received command: {command}")
            direction = command[0]
            num_pulses = int(command[1:])
            motor.move_motor(direction, num_pulses)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    motor = StepperMotorController(step_pin=17, dir_pin=27, enable_pin=22)

    try:
        kafka_consumer(motor)
    except KeyboardInterrupt:
        pass
    finally:
        motor.cleanup()
