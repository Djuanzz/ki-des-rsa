import random

class RSA:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def generate_prime_number(self, lower=2, upper=1000):
        while True:
            prime = random.randint(lower, upper)
            if self.is_prime(prime):
                return prime

    def is_prime(self, num):
        """Check if a number is prime."""
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def modinv(self, phi, m):
        for x in range(1, m):
            if (phi * x) % m == 1:
                return x
        return None

    def coprimes(self, phi):
        l = []
        for x in range(2, phi):
            if self.gcd(phi, x) == 1 and self.modinv(x, phi) != None:
                l.append(x)
            if len(l) > 5: break
        for x in l:
            if x == self.modinv(x, phi):
                l.remove(x)
        return l

    def key_generator(self):
        p = self.generate_prime_number()
        q = self.generate_prime_number()
        n = p * q
        phi = (p-1) * (q-1)  # Euler's function (totient)
        e = random.choice(self.coprimes(phi))
        d = self.modinv(e, phi)
        
        self.public_key = [e, n]
        self.private_key = [d, n]
        return self.public_key, self.private_key

    def encrypt_block(self, m, e, n):
        return (m**e) % n

    def decrypt_block(self, c, d, n):
        return (c**d) % n

    def encrypt_string(self, s, public_key):
        e, n = public_key
        return ''.join([chr(self.encrypt_block(ord(x), e, n)) for x in list(s)])

    def decrypt_string(self, s, private_key):
        d, n = private_key
        return ''.join([chr(self.decrypt_block(ord(x), d, n)) for x in list(s)])