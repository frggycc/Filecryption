# os for various functions
# hashlib to use pbkdf2_hmac
import os, sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

def generate_salt():
    return os.urandom(16)
def generate_iv():
    return os.urandom(16)

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

    # Start creating cipher and encrypting 
    plaintext = message.encode()
    enc_cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plain = pad(plaintext, 16)
    cipher_text  = enc_cipher.encrypt(padded_plain)
    return salt, cipher_text

# def decrypt_message(encrypted_message, password, salt):
#     # Generate key and extract iv and ciphertext
#     key = generate_key(password, salt)
#     iv  = encrypted_message[:16]
#     ciphertext = encrypted_message[16:]

#     # Start decrypting data
#     dec_cipher  = AES.new(key, AES.MODE_CBC, iv)
#     padded_data = dec_cipher.decrypt(cipher_text)
#     decrypted_message = unpad(padded_data, 16)
    
#     return decrypted_message

'''---------------------------------------------------------------------'''

''' Start of script '''
if __name__ == "__main__":

    # Make sure that script is used correctly
    if len(sys.argv) != 2:
        print("Usage: python3 filecryption.py <message>")
        exit()

    message = sys.argv[1]

    ''' 
    User choice menu; When begin encrypting files, will also include
    decrypting.
    '''
    print("1. Encrypt message")
    print("2. Exit")
    menu_choice = input("Enter your choice: ")

    # Get user password or exit program
    if menu_choice != "2":
        ''' *** Add password function from password library '''
        password = input("Enter Password: ")
    else:
        print("Leaving filecryption...")
        exit()

    if menu_choice == "1":
        print("Here is your message in plaintext : " + message)
        salt, cipher_text = encrypt_message(message, password)
        print("Here is your message encrypted   : ", end=" ")
        print(cipher_text)
        # decrypted_message = decrypt_message(cipher_text, password, salt)
        # print("Here is your message after decryption: " + decrypted_message)
        # exit()
