import socket
"""
Mengimpor modul socket yang digunakan untuk membuat koneksi jaringan antara klien dan server. Modul ini menyediakan berbagai fungsi untuk melakukan komunikasi melalui protokol TCP/IP."""

def gcd(a, b):
    """Menghitung Greatest Common Divisor (GCD)"""
    while b:
        a, b = b, a % b
    return a
"""
Fungsi ini menghitung GCD dari dua bilangan menggunakan algoritma Euclid. GCD adalah bilangan terbesar yang dapat membagi kedua bilangan tanpa sisa."""

def mod_inverse(e, phi):
    """Menghitung Modular Inverse dari e"""
    d = 0
    x1, x2, y1, y2 = 0, 1, 1, 0
    while e > 0:
        q = phi // e
        e, phi = phi % e, e
        x1, x2 = x2 - q * x1, x1
        y1, y2 = y2 - q * y1, y1
    return x2 + phi if phi < 0 else x2
"""
Fungsi ini menghitung invers modular dari e dengan menggunakan algoritma Extended Euclidean. Invers modular diperlukan dalam proses dekripsi RSA."""

def generate_keys(p, q):
    """Menghasilkan kunci publik dan privat"""
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Umumnya digunakan sebagai nilai e
    d = mod_inverse(e, phi)
    return (e, n), (d, n)  # Kunci publik dan privat
"""
Fungsi ini menghasilkan pasangan kunci publik dan privat untuk algoritma RSA. Kunci publik terdiri dari e dan n, sedangkan kunci privat terdiri dari d dan n. Di sini, p dan q berfungsi sebagai dua bilangan prima yang menghasilkan n. Nilai n adalah produk dari p dan q, yang digunakan dalam kedua kunci. Hal ini memastikan bahwa hanya kunci privat yang sesuai dapat mendekripsi pesan yang dienkripsi dengan kunci publik, menjaga keamanan komunikasi."""

def encrypt(message, pub_key):
    """Enkripsi pesan menggunakan kunci publik"""
    e, n = pub_key
    message_int = int.from_bytes(message.encode(), 'big')
    cipher_int = pow(message_int, e, n)
    return cipher_int
"""
Fungsi ini melakukan enkripsi pesan menggunakan kunci publik. Pesan diubah menjadi integer dan kemudian dienkripsi dengan menggunakan rumus RSA. Ini memastikan bahwa hanya penerima yang memiliki kunci privat yang dapat mendekripsi pesan tersebut, menjaga kerahasiaan komunikasi."""

def decrypt(cipher_int, priv_key):
    """Dekripsi pesan menggunakan kunci privat"""
    d, n = priv_key
    message_int = pow(cipher_int, d, n)
    return message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()
"""
Fungsi ini melakukan dekripsi pesan menggunakan kunci privat. Hasil dekripsi diubah kembali menjadi string dari bentuk integer yang terdekripsi. Ini memungkinkan penerima untuk membaca pesan asli setelah berhasil mendekripsi data yang diterima."""

if __name__ == "__main__":
    """Blok ini mengecek apakah file ini dijalankan sebagai program utama. Jika iya, maka contoh penggunaan fungsi-fungsi yang ada akan dilakukan."""
    p = 61  # Contoh bilangan prima
    q = 53  # Contoh bilangan prima
    public_key, private_key = generate_keys(p, q)
    message = "Hello"
    cipher = encrypt(message, public_key)
    print(f"Encrypted: {cipher}")
    decrypted_message = decrypt(cipher, private_key)
    print(f"Decrypted: {decrypted_message}")
"""
Di sini, dua bilangan prima p dan q didefinisikan, kunci publik dan privat dihasilkan, pesan contoh dienkripsi, dan hasilnya ditampilkan. Kemudian, pesan yang terenkripsi didekripsi dan ditampilkan juga."""
