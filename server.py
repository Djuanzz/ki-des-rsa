import socket
import threading
import random
import string
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from desAlgo import DES


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.clients = []
        self.des_keys = {}  # Store DES keys for each client

    def generate_des_key(self):
        """Generate a random 8-byte DES key."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def exchange_keys(self, client):
        try:
            # Receive client's public key
            client_public_key = client.recv(4096).decode('utf-8')
            client_rsa_key = RSA.import_key(client_public_key)
            cipher_rsa = PKCS1_OAEP.new(client_rsa_key)

            # Generate and send DES key
            des_key = self.generate_des_key()
            encrypted_des_key = cipher_rsa.encrypt(des_key.encode('utf-8'))
            client.send(encrypted_des_key)

            return des_key
        except Exception as e:
            print(f"Key exchange failed: {e}")
            return None

    def broadcast(self, message, des_key):
        for client in self.clients:
            try:
                des = DES(des_key)
                encrypted_message = des.encrypt(message)
                client.send(encrypted_message)
            except Exception as e:
                print(f"Failed to send message to a client: {e}")
                self.remove_client(client)

    def handle_client(self, client):
        des_key = self.exchange_keys(client)
        if not des_key:
            self.remove_client(client)
            return

        print(f"DES key established for a client: {des_key}")

        while True:
            try:
                # Receive and decrypt message
                encrypted_message = client.recv(1024)
                des = DES(des_key)
                decrypted_message = des.decrypt(encrypted_message)
                print(f"Received: {decrypted_message}")

                # Broadcast the decrypted message to all clients
                self.broadcast(decrypted_message, des_key)
            except:
                print("A client disconnected or an error occurred!")
                self.remove_client(client)
                break

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
            client.close()

    def receive_connections(self):
        print(f"Server is running on {self.host}:{self.port}...")
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            self.clients.append(client)

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 55555

    chat_server = Server(HOST, PORT)
    chat_server.receive_connections()
