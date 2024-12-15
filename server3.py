from socket import *
from threading import Thread

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.client_sockets = []
        self.client_addresses = {}
        self.public_keys = []
        self.buffer_size = 1024

    def accept_incoming_connections(self):
        while len(self.client_sockets) < 2:
            client, client_address = self.server_socket.accept()
            self.client_sockets.append(client)
            print(f"{client_address} has connected.")
            public_key = client.recv(self.buffer_size).decode('utf-8')
            self.public_keys.append(public_key)
            self.client_addresses[client] = client_address
            if len(self.client_sockets) == 2:
                self.client_sockets[0].send(self.public_keys[1].encode('utf-8'))
                self.client_sockets[1].send(self.public_keys[0].encode('utf-8'))

    def handle_client(self, client, client_idx):
        try:
            while True:
                msg = client.recv(self.buffer_size).decode('utf-8')
                if msg:
                    print(f"Client {client_idx + 1}: {msg}")
                    other_client_idx = 1 - client_idx
                    self.client_sockets[other_client_idx].send(msg.encode('utf-8'))
                else:
                    break
        except ConnectionResetError:
            print(f"Client {client_idx + 1} has disconnected.")
        finally:
            client.close()

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)

        print(f"Server is running on {self.host}:{self.port}")
        print("Waiting for connections...")

        self.accept_incoming_connections()

        for idx, client in enumerate(self.client_sockets):
            Thread(target=self.handle_client, args=(client, idx)).start()

        print("Encrypted conversation started.")
        self.server_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345
    server = ChatServer(host, port)
    server.start_server()
