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

def get_authentication(filetype):
    filename = input("Enter the filename : " )

    # If encrypted file exists, ask to overwrite
    if file_exist(filename, filetype): # Check if file exists
        print("Encryption/Decryption file already exists!")
        proceed = input("Would you like to proceed? (y/n): ")
        if proceed == "n" or proceed == "N":
            exit()
    else:
        print("Filename doesn't exist!")
        exit()
    
    password = getpass.getpass("Enter your password: ")

    print("")

def file_exist(filename, file_ext):
    if not os.path.exists(filename):
        return False
    return True

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

    # # Make sure that script is used correctly
    # if len(sys.argv) != 2:
    #     print("Usage: python3 filecryption.py")
    #     exit()

    ''' 
    User choice menu; When begin encrypting files, will also include
    decrypting.
    '''
    print("1. Encrypt/Decrypt Messages (Demo)")
    print("2. Encrypt File")
    print("3. Decrypt File")
    print("4. Exit")
    menu_choice = input("Enter your choice: ")
    print("-"*40 + "\n")

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
        print("Encrypt File...\n")
        filename, password = get_authentication(ENCODE_EXT)
        print("Encrypting your file...")
        encrypt_file(filename, password)

    elif menu_choice == "3":
        print("Decrypt File...\n")
        filename, password = get_authentication(DECODE_EXT)
        print("Decrypting your file...")
        decrypt_file(filename, password)

    else:
        print("Not a valid choice. Exiting...")
        exit()
    





