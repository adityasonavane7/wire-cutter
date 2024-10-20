import zmq
import RPi.GPIO as GPIO
import time

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
            GPIO.output(self.enable_pin, GPIO.HIGH)  # Enable the motor driver

    def set_direction(self, direction):
        GPIO.output(self.dir_pin, GPIO.HIGH if direction == '+' else GPIO.LOW)

    def send_pulse(self, steps):
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(0.01)  # Adjust for speed
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(0.01)

    def move_motor(self, direction, steps):
        self.set_direction(direction)
        self.send_pulse(steps)

    def cleanup(self):
        GPIO.cleanup()

def main():
    # Create a ZeroMQ context
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # REP socket for replies
    socket.bind("tcp://*:5555")  # Bind to port 5555

    motor = StepperMotorController(step_pin=22, dir_pin=17, enable_pin=27)  # Use GPIO pin numbers

    print("Waiting for commands...")
    while True:
        message = socket.recv_string()  # Receive a command
        print(f"Received command: {message}")

        if message.startswith('+') or message.startswith('-'):
            direction = message[0]
            steps = abs(int(message[1:]))  # Get the absolute value of steps
            motor.move_motor(direction, steps)
            socket.send_string(f"Moved {direction} {steps} steps")  # Reply back
        else:
            socket.send_string("Invalid command")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        motor.cleanup()