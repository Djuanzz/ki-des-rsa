import socket
from des_algorithm import generate_keys, encrypt
"""
Mengimpor modul socket untuk komunikasi jaringan dan fungsi generate_keys serta encrypt dari des_algorithm.py untuk menghasilkan kunci dan melakukan enkripsi pesan."""

def send_message(message, pub_key):
    """Mengirim pesan terenkripsi ke server"""
    # Buat socket klien
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))
    """
    Fungsi ini membuat socket klien dan menghubungkannya ke server yang berjalan di localhost pada port 5000. Socket ini akan digunakan untuk mengirim data ke server."""
    
    # Enkripsi pesan
    cipher = encrypt(message, pub_key)
    """
    Pesan yang dimasukkan pengguna dienkripsi menggunakan kunci publik yang diberikan, menghasilkan pesan terenkripsi yang siap untuk dikirim."""
    
    # Kirim pesan terenkripsi
    client.send(str(cipher).encode())
    print(f"Sent encrypted message: {cipher}")
    client.close()
    """
    Pesan terenkripsi dikirim ke server, dan koneksi socket ditutup setelah pengiriman selesai."""
 
if __name__ == "__main__":
    """Blok ini mengecek apakah file ini dijalankan sebagai program utama. Jika iya, maka proses pengiriman pesan akan dilakukan."""
    p = 61  # Bilangan prima
    q = 53  # Bilangan prima
    public_key = generate_keys(p, q)[0]
    """
    Dua bilangan prima didefinisikan, dan kunci publik dihasilkan dengan memanggil fungsi generate_keys. Nilai n, yang merupakan hasil kali p dan q, digunakan dalam kunci publik untuk enkripsi. Dengan menggunakan kunci publik ini, pesan dapat dienkripsi dengan aman sebelum dikirim ke server."""
    
    message = input("Enter message to encrypt and send: ")
    send_message(message, public_key)
    """
    Pengguna diminta untuk memasukkan pesan yang ingin dienkripsi dan dikirim. Fungsi send_message akan dipanggil untuk mengirimkan pesan tersebut."""
