import sys
import base64
import json
import os
import hashlib
import getpass
from Crypto.Cipher import AES # type: ignore
from Crypto.Util.Padding import pad # type: ignore
from Crypto.Util.Padding import unpad # type: ignore

CONFIG_FILE = ".encryption_file"
ENCODE_EXT  = ".enc"
DECODE_EXT  = ".dec"

def get_file_info(extension):
    filename = input("Enter the filename: " )

    # Check; Does encrypted file of it exist?
    if file_exist(filename + extension):
        get_authorization()
        password = getpass.getpass("Enter your password: ")
    elif file_exist(filename):
        password = getpass.getpass("Enter your password: ")
        print("")
    else:
        print("File does not exist!")
        exit()

    return filename, password

def get_authorization():
    print("\n  .................. !!!!! ...................")
    print("    Encrypted/Decrypted file already exists!")
    proceed = input("    Would you like to proceed? (y/n): ")

    if proceed == "n" or proceed == "N":
        exit()

    print("  ............................................\n")

def file_exist(name):
    if os.path.exists(name):
        return True
    return False

def generate_salt():
    return os.urandom(16)

def generate_key_and_iv(password, salt):
    # Hash algorithm, passphrase, salt, iterations, key len in bytes
    derived_key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 10000, 48)
    key = derived_key[:32]
    iv  = derived_key[32:]
    return key, iv
    
'''---------------------------------------------------------------------'''
''' Used for testing successful encrypting and decrypting '''
def encrypt_message(message, password):
    # Generate necessary values
    salt    = generate_salt()
    key, iv = generate_key_and_iv(password, salt)

    # Pad message and start encrypting
    padded_message = pad(message.encode(), AES.block_size)
    enc_cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_message  = enc_cipher.encrypt(padded_message)

    return salt, iv, encrypted_message

def decrypt_message(encrypted_message, password, salt):
    # Regenerate key and iv
    key, iv = generate_key_and_iv(password, salt)
    
    # Start decrypting data
    dec_cipher  = AES.new(key, AES.MODE_CBC, iv)
    padded_data = dec_cipher.decrypt(encrypted_message)
    decrypted_message = unpad(padded_data, AES.block_size)
    
    return decrypted_message.decode()

'''---------------------------------------------------------------------'''
''' Used to encrypt and decrypt files Python can natively open and modify '''
def encrypt_file(filename, password):
    # Generate necessary values
    salt    = generate_salt()
    key, iv = generate_key_and_iv(password, salt)

    # Read data from file; binary mode to start padding and encrypting
    with open(filename, 'rb') as file:
        data = file.read()

    # Pad message and start encrypting
    padded_data = pad(data, AES.block_size)
    enc_cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = enc_cipher.encrypt(padded_data)

    encrypted_file = filename + ENCODE_EXT
    with open(encrypted_file, "wb") as file:
        file.write(encrypted_data)

    # Update the config file, if exist; Otherwise, create one
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    else:
        config = {}

    # Use dictionary to store filenames and salt information
    config[filename] = base64.b64encode(salt).decode()

    # Write updated dictionary to json file
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent = 4)
    
    if os.path.exists(CONFIG_FILE):
        print("File encrypted successfully as " + encrypted_file)
        print("Encryption information stored in " + CONFIG_FILE)

def decrypt_file(filename, password):
    # Load config into local variable
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    else:
        config = {}
    
    # See if the key exists in the config file/variable
    if filename not in config:
        print("Key for ", filename, " not found.")
        return
    
    # Check if proper ".enc" file exists in directory for filenmame
    encrypted_file = filename + ENCODE_EXT
    if not os.path.exists(encrypted_file):
        print("Encrypted file" + encrypted_file + "not found!")
        return

    # All points checked, get key 
    salt    = base64.b64decode(config[filename])
    key, iv = generate_key_and_iv(password, salt)

    # Read encrypted file
    with open(encrypted_file, "rb") as file:
        encrypted_data = file.read()
    
    dec_cipher = AES.new(key, AES.MODE_CBC, iv)

    try:
        decrypted_data = dec_cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_data, AES.block_size)

        decrypted_file = filename + DECODE_EXT
        with open (decrypted_file, "wb") as file:
            file.write(decrypted_data)

        print("File decrypted successfully.")

    except ValueError:
        print("Decryption failed or corrupted file.")


''' Start of script '''
if __name__ == "__main__":

    ''' 
    User choice menu; When begin encrypting files, will also include
    decrypting.
    '''
    print("1. Encrypt/Decrypt Messages (Demo)")
    print("2. Encrypt File")
    print("3. Decrypt File")
    print("4. Exit")
    menu_choice = input("Enter your choice: ")

    # Exit program
    if menu_choice == "1":
        print("Encrypt/Decrypt Messages (Demo)...\n")
        message  = str(input("Enter your message : "))
        password = getpass.getpass("Enter your password: ")

        print("")

        print("Here is your message (plaintext) : " + message)
        salt, iv, encrypted_message = encrypt_message(message, password)
        print("Here is your message encrypted   :", end=" ")
        print(encrypted_message)
        decrypted_message = decrypt_message(encrypted_message, password, salt)
        print("Message after decryption         : " + decrypted_message)

    elif menu_choice == "2":
        os.system('clear')
        print("\nEncrypt File")
        print("-"*40)

        filename, password = get_file_info(ENCODE_EXT)

        encrypt_file(filename, password)

    elif menu_choice == "3":
        os.system('clear')
        print("\nDecrypt File")
        print("-"*40)
        filename, password = get_file_info(DECODE_EXT)
        
        decrypt_file(filename, password)

    else:
        print("Not a valid choice. Exiting...")
        exit()
    





