import random
from math import gcd

class RSACUY :
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def random_print(self):
        print("Hello, World! ini dari rsa.py")
    
    def encrypt(self, message, public_key):
        e, n = public_key
        encrypted_message = [pow(ord(char), e, n) for char in message]
        return encrypted_message
    
    def decrypt(self, encrypted_message):
        d, n = self.private_key
        decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
        return decrypted_message
    
    def encoder(self, message):
        encoded = []
        for char in message:
            encoded.append(ord(char))
        return encoded
    
    def decoder(self, encoded):
        decoded = ''
        for num in encoded:
            decoded += chr(self.decrypt(num))
        return decoded

    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def generate_prime_number(self):
        while True:
            prime = random.randint(100, 1000)
            if self.is_prime(prime):
                return prime

    def generate_rsa_keys(self):
        p = self.generate_prime_number()
        q = self.generate_prime_number()

        n = p * q
        phi = (p - 1) * (q - 1)

        e = random.randint(1, phi)
        while gcd(e, phi) != 1:
            e = random.randint(1, phi)

        d = 0
        while (d * e) % phi != 1:
            d += 1

        self.private_key = (d, n)
        self.public_key = (e, n)

