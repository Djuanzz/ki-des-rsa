import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from desAlgo import DES

class Client:
    def __init__(self, cliId, server_host, server_port, pka_host, pka_port):
        self.server_host = server_host
        self.server_port = server_port
        self.pka_host = pka_host
        self.pka_port = pka_port
        self.cliId = cliId
        self.algo = DES()
        self.key_des = None
        self.key_des_bin = None
        self.rkb = None
        self.rk = None
        self.rk_rev = None
        self.rkb_rev = None

        # Connect to server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_host, self.server_port))

        # Generate RSA keys
        self.generate_rsa_keys()

    def generate_rsa_keys(self):
        """Generate RSA key pair."""
        self.private_key = RSA.generate(2048)  # Generate 2048 bit key
        self.public_key = self.private_key.publickey()

    def send_public_key_to_pka(self):
        """Send the public key to the PKA."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pka_client:
                pka_client.connect((self.pka_host, self.pka_port))

                # Format data (Client ID and Public Key)
                data = f"STORE::{self.cliId}::{self.public_key.exportKey().decode('utf-8')}"
                pka_client.send(data.encode('utf-8'))
                # print(f"Public key sent to PKA for {self.cliId}.")

                # Receive acknowledgment
                response = pka_client.recv(1024).decode('utf-8')
                print(f"PKA response: {response}")
        except Exception as e:
            print("Error sending public key to PKA:", e)

    def request_public_key(self, target_cli_id):
        """Request the public key of another client."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pka_client:
                pka_client.connect((self.pka_host, self.pka_port))
                request_message = f"REQUEST::{target_cli_id}"
                pka_client.send(request_message.encode('utf-8'))
                response = pka_client.recv(4096).decode('utf-8')
                if response.startswith("Public key for"):
                    print(f"Error: {response}")
                    return None
                # print(f"Received public key for {target_cli_id}:\n{response}")
                return response
        except Exception as e:
            print("Error requesting public key from PKA:", e)
            return None

    def encrypt_message(self, message, public_key):
        """Encrypt message using RSA public key."""
        try:
            rsa_public_key = RSA.import_key(public_key.encode('utf-8'))
            self.key_des = input("Enter DES key: ")
            self.key_des_bin = self.algo.ascii_to_bin(self.key_des)
            self.rkb, self.rk = self.algo.generate_keys(self.key_des_bin)
            self.rk_rev = self.rk[::-1]
            self.rkb_rev = self.rkb[::-1]

            message = self.algo.ascii_to_bin(message)
            encrypted_message = self.algo.encrypt(message, self.rkb, self.rk)
            encrypted_message = encrypted_message.encode('utf-8')
            # cipher = PKCS1_OAEP.new(rsa_public_key)
            # encrypted_message = cipher.encrypt(message.encode('utf-8'))
            return encrypted_message
        except Exception as e:
            print("Encryption error:", e)
            return None

    def decrypt_message(self, encrypted_message):
        """Decrypt message using RSA private key."""
        try:
            # cipher = PKCS1_OAEP.new(self.private_key)
            # decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
            decrypted_message = self.algo.decrypt(encrypted_message.decode('utf-8'), self.rkb_rev, self.rk_rev)
            decrypted_message = self.algo.bin_to_ascii(decrypted_message)
            return decrypted_message
        except Exception as e:
            print("Decryption error:", e)
            return None

    def receive(self):
        """Receive messages from server."""
        while True:
            try:
                encrypted_message = self.client.recv(1024)
                if not encrypted_message:
                    break
                # print(f"Encrypted message received: {encrypted_message}")

                # Decrypt the message
                decrypted_message = self.decrypt_message(encrypted_message)
                print(f"Decrypted message: {decrypted_message}")
            except Exception as e:
                print("An error occurred while receiving the message!", e)
                self.client.close()
                break

    def write(self):
        """Write and send messages."""
        while True:
            try:
                target_id = input("Enter recipient ID: ")
                target_public_key = self.request_public_key(target_id)
                if not target_public_key:
                    print("Failed to retrieve public key.")
                    continue

                message = input("Message: ")
                encrypted_message = self.encrypt_message(message, target_public_key)
                if not encrypted_message:
                    print("Failed to encrypt the message.")
                    continue

                self.client.send(encrypted_message)
                print(f"Encrypted message sent to {target_id}.")
            except Exception as e:
                print("An error occurred during sending!", e)
                break

    def start(self):
        """Start the client and communication threads."""
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
