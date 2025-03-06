# os for various functions
# hashlib to use pbkdf2_hmac
import os, sys
import hashlib
import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

def generate_salt():
    return os.urandom(16)
def generate_iv():
    return os.urandom(16)

''' 
Testing: Make key size to 32; The first half for the AES key
and the second half for the IV; This makes it so we don't need to keep track
of the IV in a file.
'''
def generate_key(password, salt):
    # Hash algorithm, passphrase, salt, iterations, key len in bytes
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 10000, 32)
    return key

'''---------------------------------------------------------------------'''
''' Used for testing successful encrypting and decrypting '''
def encrypt_message(message, password):
    # Generate necessary 
    salt = generate_salt()
    iv   = generate_iv()
    key  = generate_key(password, salt)

    # Pad message and start encrypting
    padded_message = pad(message.encode(), AES.block_size)
    enc_cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_message  = enc_cipher.encrypt(padded_message)

    return salt, iv, encrypted_message

def decrypt_message(encrypted_message, password, salt, iv):
    # Generate key and extract iv and ciphertext
    key = generate_key(password, salt)
    
    # Start decrypting data
    dec_cipher  = AES.new(key, AES.MODE_CBC, iv)
    padded_data = dec_cipher.decrypt(encrypted_message)
    decrypted_message = unpad(padded_data, AES.block_size)
    
    return decrypted_message.decode()

'''---------------------------------------------------------------------'''

''' Start of script '''
if __name__ == "__main__":

    # Make sure that script is used correctly
    if len(sys.argv) != 2:
        print("Usage: python3 filecryption.py <message>")
        exit()

    message  = sys.argv[1]

    ''' 
    User choice menu; When begin encrypting files, will also include
    decrypting.
    '''
    print("1. Encrypt Messages (Demo)")
    print("2. Exit")
    menu_choice = input("Enter your choice: ")

    # Get user password or exit program
    if menu_choice == "1":
        password = getpass.getpass("Enter Password: ")
    else:
        print("Leaving filecryption...")
        exit()

    if menu_choice == "1":
        print("-"*12 + "\nTesting out encryption/decryption...\n")
        print("Here is your message (plaintext) : " + message)
        salt, iv, encrypted_message = encrypt_message(message, password)
        print("Here is your message encrypted   :", end=" ")
        print(encrypted_message)
        decrypted_message = decrypt_message(encrypted_message, password, salt, iv)
        print("Here is your message after decryption: " + decrypted_message)


