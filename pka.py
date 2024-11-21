import socket
import threading

class PublicKeyAuthority:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        # Dictionary to store client public keys
        self.public_keys = {}
        print(f"PKA is running on {self.host}:{self.port}...")

    def handle_client(self, client):
        try:
            # Receive public key and client ID
            data = client.recv(4096).decode('utf-8')
            cli_id, public_key = data.split('::', 1)
            print(f"Received public key from {cli_id}:\n{public_key}")

            # Store the public key
            self.public_keys[cli_id] = public_key
            print(f"Stored public key for {cli_id}.")

            # Send acknowledgment back to the client
            client.send(f"Public key for {cli_id} stored successfully.".encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client.close()

    def start(self):
        """Start the PKA server."""
        while True:
            client, address = self.server.accept()
            print(f"Connected with {address}")
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432  # PKA listens on a different port from the Server

    pka = PublicKeyAuthority(HOST, PORT)
    pka.start()
