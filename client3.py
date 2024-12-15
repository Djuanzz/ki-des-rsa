import socket
import sys
from threading import Thread
from rsa import RSA


class ChatClient:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.buffer_size = 1024
        self.address = (self.host, self.port)

        # Initialize RSA and generate keys
        self.rsa = RSA()
        self.rsa.generate_rsa_keys()
        self.public_key = self.rsa.public_key
        self.private_key = self.rsa.private_key

        # Initialize client socket
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.address)
        except ConnectionRefusedError:
            print("Failed to connect to the server. Please ensure the server is running.")
            sys.exit(1)

        # Send public key to server
        public_key_msg = f"{self.public_key[0]}*{self.public_key[1]}"
        self.client.send(public_key_msg.encode('utf8'))

        # Receive server's public key
        server_key_msg = self.client.recv(self.buffer_size).decode('utf8')
        self.server_public_key = tuple(map(int, server_key_msg.split('*')))

        # Start receive thread
        self.receive_thread = Thread(target=self.receive, daemon=True)
        self.receive_thread.start()

    def receive(self):
        """Handle incoming messages."""
        print(f"Welcome {self.name}! You are now online.")
        while True:
            try:
                encrypted_msg = self.client.recv(self.buffer_size)
                if not encrypted_msg:
                    continue
                # Decrypt the incoming message
                encrypted_msg = list(map(int, encrypted_msg.decode('utf8').split(',')))
                msg = self.rsa.decrypt(encrypted_msg)
                print(msg)
            except OSError:
                print("Connection to server lost.")
                break

    def send(self):
        """Send messages to the server."""
        while True:
            try:
                msg = input(f"{self.name}: ").strip()
                if not msg:
                    continue  # Skip empty messages
                formatted_msg = f"{self.name}: {msg}"
                # Encrypt the message using server's public key
                encrypted_msg = self.rsa.encrypt(formatted_msg, self.server_public_key)
                encrypted_msg_str = ','.join(map(str, encrypted_msg))
                self.client.send(encrypted_msg_str.encode('utf8'))
            except (KeyboardInterrupt, EOFError):
                self.on_closing()
                break

    def on_closing(self):
        """Handle client closing."""
        print("\nGoing offline...")
        try:
            self.client.close()
        except OSError:
            pass
        sys.exit(0)

    def start(self):
        """Start the client."""
        try:
            self.send()
        except KeyboardInterrupt:
            self.on_closing()


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    name = input('Enter your name: ').strip()

    if not name:
        print("Name cannot be empty. Exiting.")
        sys.exit(1)

    chat_client = ChatClient(host, port, name)
    chat_client.start()
