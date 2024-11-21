import socket
import threading
from Crypto.PublicKey import RSA
from desAlgo import DES


class Client:
    def __init__(self, cliId, server_host, server_port, pka_host, pka_port):
        self.server_host = server_host
        self.server_port = server_port
        self.pka_host = pka_host
        self.pka_port = pka_port
        self.cliId = cliId
        self.des_algo = DES()

        # Connect to server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_host, self.server_port))

    def generate_rsa_keys(self):
        """Generate RSA key pair."""
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.publickey()

    def send_public_key_to_pka(self):
        """Send the public key to the PKA."""
        try:
            pka_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pka_client.connect((self.pka_host, self.pka_port))

            # Prepare data (Client ID and Public Key)
            data = f"{self.cliId}::{self.public_key.exportKey().decode('utf-8')}"
            pka_client.send(data.encode('utf-8'))
            print(f"Public key sent to PKA for {self.cliId}.")

            # Receive acknowledgment
            response = pka_client.recv(1024).decode('utf-8')
            print(f"PKA response: {response}")
        except Exception as e:
            print("Error sending public key to PKA:", e)
        finally:
            pka_client.close()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                print(message)
            except Exception as e:
                print("An error occurred!", e)
                self.client.close()
                break

    def write(self):
        while True:
            try:
                message = input()
                self.client.send(message.encode('utf-8'))
            except Exception as e:
                print("An error occurred during sending!", e)
                break

    def start(self):
        # Generate RSA keys
        self.generate_rsa_keys()

        # Send public key to PKA
        self.send_public_key_to_pka()

        # Start threads for communication with server
        receive_thread = threading.Thread(target=self.receive)
        write_thread = threading.Thread(target=self.write)

        receive_thread.start()
        write_thread.start()


if __name__ == "__main__":
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 55555  # Server port
    PKA_HOST = '127.0.0.1'
    PKA_PORT = 65432  # PKA port
    CLI_ID = input("Client ID: ")

    client = Client(CLI_ID, SERVER_HOST, SERVER_PORT, PKA_HOST, PKA_PORT)
    client.start()
