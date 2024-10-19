# Define variables
IMAGE_NAME = stepper_controller_image
CONTAINER_NAME = stepper_controller_container

# Default target
all: build run

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run --name $(CONTAINER_NAME) --network host -it --privileged \
		--device /dev/gpiomem \
		-v /sys/class/gpio:/sys/class/gpio \
		$(IMAGE_NAME)

# Clean up the container and image
clean:
	docker rm -f $(CONTAINER_NAME) || true
	docker rmi -f $(IMAGE_NAME) || true

.PHONY: all build run clean