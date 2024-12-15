import socket
import sys
import time
from threading import Thread
from rsa import RSA

class ChatClient:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.buffer_size = 1024
        self.address = (self.host, self.port)

        self.rsa = RSA()
        public_key, private_key = self.rsa.key_generator()
        self.public_key = public_key
        self.private_key = private_key

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address)

        public_key_1 = self.public_key
        msg = f"{public_key_1[0]}*{public_key_1[1]}"
        self.client.send(bytes(msg, "utf8"))

        m = self.client.recv(self.buffer_size).decode('utf8')
        self.public_key_2 = [int(x) for x in m.split('*')]

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        print(f"Welcome! {self.name}")
        print("You are online!")
        while True:
            try:
                msg = self.client.recv(self.buffer_size).decode("utf8")
                msg = self.rsa.decrypt_string(msg, self.private_key)
                print(msg)
            except OSError:
                break

    def send(self):
        msg = input(f"{self.name}: ")
        msg = f"{self.name}: {msg}"
        print(msg)
        encrypted_msg = self.rsa.encrypt_string(msg, self.public_key_2)
        self.client.send(bytes(encrypted_msg, "utf8"))

    def on_closing(self):
        print("Going offline...")
        time.sleep(2)
        self.client.close()
        sys.exit()

    def start(self):
        try:
            while True:
                self.send()
        except KeyboardInterrupt:
            self.on_closing()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    name = input('Enter your name: ')
    
    chat_client = ChatClient(host, port, name)
    chat_client.start()
