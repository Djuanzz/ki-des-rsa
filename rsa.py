import random
from math import gcd

class RSA:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def generate_prime_number(self, lower=100, upper=1000):
        while True:
            prime = random.randint(lower, upper)
            if self.is_prime(prime):
                return prime

    def mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            a, m = m, a % m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def generate_rsa_keys(self):
        p = self.generate_prime_number()
        q = self.generate_prime_number()
        n = p * q
        phi = (p - 1) * (q - 1)

        e = random.randrange(2, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(2, phi)

        d = self.mod_inverse(e, phi)

        self.public_key = (e, n)
        self.private_key = (d, n)

    def encrypt(self, message, public_key):
        e, n = public_key
        return [pow(ord(char), e, n) for char in message]

    def decrypt(self, encrypted_message):
        d, n = self.private_key
        return ''.join([chr(pow(char, d, n)) for char in encrypted_message])
