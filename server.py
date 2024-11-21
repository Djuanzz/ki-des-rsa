import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []  # Daftar untuk menyimpan klien yang terhubung
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server is running on {self.host}:{self.port}...")

    def broadcast(self, message, client_to_ignore=None):
        """Broadcast pesan ke semua klien kecuali klien yang mengirim pesan."""
        for client in self.clients:
            if client != client_to_ignore:
                try:
                    client.send(message)  # Mengirim pesan ke klien lainnya
                except Exception as e:
                    print(f"Error sending message to client: {e}")
                    self.remove_client(client)

    def handle_client(self, client, address):
        """Menangani komunikasi dengan setiap klien."""
        try:
            print(f"Client connected from {address}")
            client.send("Welcome to the chat server!".encode('utf-8'))  # Kirim pesan selamat datang

            while True:
                data = client.recv(4096)
                if not data:
                    break  # Tidak ada data, client disconnect
                # print(f"Received data from {address}: {data}")

                # Jika data berupa pesan, broadcast ke semua client
                self.broadcast(data, client)  # Kirim pesan ke semua klien kecuali pengirim

            self.remove_client(client)
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            self.remove_client(client)
        finally:
            client.close()

    def remove_client(self, client):
        """Menghapus client dari daftar jika terputus."""
        if client in self.clients:
            self.clients.remove(client)
            print("Client removed successfully.")

    def start(self):
        """Memulai server dan mendengarkan koneksi klien baru."""
        while True:
            client, address = self.server.accept()
            self.clients.append(client)  # Menambahkan client ke daftar
            print(f"New connection: {address}")
            thread = threading.Thread(target=self.handle_client, args=(client, address))
            thread.start()


if __name__ == "__main__":
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 55555
    server = Server(SERVER_HOST, SERVER_PORT)
    server.start()
