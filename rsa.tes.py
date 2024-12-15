from rsa import RSA

if __name__ == "__main__":
    rsa = RSA()
    public_key, private_key = rsa.key_generator()
    message = "110001000101011"
    encrypted_message = rsa.encrypt_string(message, public_key)
    decrypted_message = rsa.decrypt_string(encrypted_message, private_key)

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)