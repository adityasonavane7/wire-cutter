import sys
import zmq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main(message):
    # Create a ZeroMQ context
    context = zmq.Context()
    logging.info("Initializing ZeroMQ context.")

    # Create a REQ socket
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")  # Adjust to your receiver's address
    logging.info("Connected to ZeroMQ receiver at tcp://localhost:5555")

    try:
        # Send the message
        logging.info(f"Sending message: {message}")
        socket.send_string(message)

        # Wait for the response
        response = socket.recv_string()
        logging.info(f"Received response: {response}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Clean up
        socket.close()
        context.term()
        logging.info("Closed ZeroMQ socket and terminated context.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python zmq_sender.py <message>")
        sys.exit(1)

    message = sys.argv[1]
    main(message)