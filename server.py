import socket
from des_algorithm import generate_keys, decrypt
"""
Mengimpor modul socket untuk komunikasi jaringan dan fungsi generate_keys serta decrypt dari des_algorithm.py untuk menghasilkan kunci dan mendekripsi pesan yang diterima."""
 
def start_server():
    """Memulai server untuk menerima pesan"""
    # Membuat socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(1)
    print("Server listening on port 5000...")
    """
    Fungsi ini membuat socket server, mengikatnya ke alamat localhost pada port 5000, dan mulai mendengarkan koneksi dari klien. Informasi bahwa server sedang aktif akan ditampilkan."""
    
    # Menghasilkan kunci
    p = 61  # Bilangan prima
    q = 53  # Bilangan prima
    private_key = generate_keys(p, q)[1]
    """
    Dua bilangan prima didefinisikan, dan kunci privat dihasilkan menggunakan fungsi generate_keys. Nilai n, yang merupakan hasil kali p dan q, digunakan dalam kunci privat untuk dekripsi. Kunci ini memungkinkan server untuk mendekripsi pesan yang diterima dari klien dengan aman."""
    
    while True:
        client, address = server.accept()
        print(f"Connection from {address} established")
        """
        Server akan terus-menerus menerima koneksi dari klien. Saat koneksi diterima, informasi alamat klien akan ditampilkan."""
        
        # Menerima pesan terenkripsi
        encrypted_message = client.recv(1024).decode()
        print(f"Received encrypted message: {encrypted_message}")
        """
        Pesan terenkripsi diterima dari klien dan ditampilkan. Server akan menunggu hingga 1024 byte data diterima."""
        
        # Dekripsi pesan
        decrypted_message = decrypt(int(encrypted_message), private_key)
        print(f"Decrypted message: {decrypted_message}")
        """
        Pesan terenkripsi didekripsi menggunakan kunci privat. Hasil dekripsi kemudian ditampilkan ke konsol."""
        
        client.close()
        """
        Setelah memproses pesan, koneksi klien ditutup untuk menghemat sumber daya."""
 
if __name__ == "__main__":
    start_server()
    """Blok ini menjalankan fungsi start_server jika file ini dijalankan sebagai program utama, memulai server untuk mendengarkan pesan dari klien."""
