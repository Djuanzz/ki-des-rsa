import socket
import sys
from threading import Thread
from rsa import RSA
from desAlgo import DES


class ChatClient:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.buffer_size = 1024
        self.address = (self.host, self.port)

        self.des = DES()
        self.key_des = "sipsipok"
        self.key_des_bin = self.des.ascii_to_bin(self.key_des)
        self.rkb, self.rk = self.des.generate_keys(self.key_des_bin)
        self.rk_rev = self.rk[::-1]
        self.rkb_rev = self.rkb[::-1]

        self.rsa = RSA()
        self.rsa.generate_rsa_keys()
        self.public_key = self.rsa.public_key
        self.private_key = self.rsa.private_key

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.address)
        except ConnectionRefusedError:
            print("Failed to connect to the server. Please ensure the server is running.")
            sys.exit(1)

        public_key_msg = f"{self.public_key[0]}*{self.public_key[1]}"
        self.client.send(public_key_msg.encode('utf-8'))

        server_key_msg = self.client.recv(self.buffer_size).decode('utf-8')
        self.server_public_key = tuple(map(int, server_key_msg.split('*')))

        self.receive_thread = Thread(target=self.receive, daemon=True)
        self.receive_thread.start()

    def receive(self):
        print(f"Welcome {self.name}! You are now online.")
        while True:
            try:
                encrypted_msg = self.client.recv(self.buffer_size)
                if not encrypted_msg:
                    continue
                encrypted_msg = encrypted_msg.decode('utf-8')
                encrypted_msg = list(map(int, encrypted_msg.split(',')))
                # print(encrypted_msg)
                encrypted_msg = self.rsa.decrypt(encrypted_msg)
                # print(encrypted_msg)
                encrypted_msg = self.des.decrypt(encrypted_msg, self.rkb_rev, self.rk_rev)
                msg = self.des.bin_to_ascii(encrypted_msg)
                print(msg)
            except OSError:
                print("Connection to server lost.")
                break

    def send(self):
        while True:
            try:
                msg = input(f"{self.name}: ").strip()
                if not msg:
                    continue  # Skip empty messages
                msg = self.des.ascii_to_bin(msg)
                msg = self.des.encrypt(msg, self.rkb, self.rk)
                encrypted_msg = self.rsa.encrypt(msg, self.server_public_key)
                encrypted_msg = list(map(str, encrypted_msg))
                encrypted_msg = ','.join(encrypted_msg)
                # print(encrypted_msg)
                self.client.send(encrypted_msg.encode('utf-8'))
            except (KeyboardInterrupt, EOFError):
                self.on_closing()
                break

    def on_closing(self):
        print("\nGoing offline...")
        try:
            self.client.close()
        except OSError:
            pass
        sys.exit(0)

    def start(self):
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
