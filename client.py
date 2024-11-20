import socket
import threading
from desAlgo import DES

algo = DES()
key = "AMANAJAA"
key_bin = algo.ascii_to_bin(key)
rkb, rk = algo.generate_keys(key_bin)
rkb_rev = rkb[::-1]
rk_rev = rk[::-1]

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            decrypted_res = algo.bin_to_ascii(algo.decrypt(message, rkb_rev, rk_rev))
            print(decrypted_res)

        except Exception as e:
            # Close Connection When Error
            print("An error occured!", e)
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = input()
        msg_bin = algo.ascii_to_bin(message)
        encrypted_msg = algo.encrypt(msg_bin, rkb, rk)

        client.send(encrypted_msg.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
