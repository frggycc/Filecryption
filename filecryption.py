# os for random salt
# hashlib to use pbkdf2_hmac
import sys, os
import hashlib, binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

# Get action, file location, password to use
# i.e. encrypt example.txt SuperStrongPassword
# ACTION = str(sys.argv[1])
# FILE   = str(sys.argv[2])
# PASS   = str(sys.argv[3])
# LENGTH = str(sys.argv[4])

MESSAGE = str(sys.argv[1])
PASS    = str(sys.argv[2])

''' 
CREATING AES KEY FROM PASSPHRASES
-----------------------------------------------------------------------
Passphrase can be of any length. For the purpose of starting out this
project, all key lengths will be 16-bytes so regardless of the
passphrase size, the key generated will 16-bytes.

Additionally, we will make use of salting to make sure each time a key
is generated using the passphrase, each key will be different from
one another. Only the salt and the encrypted plaintext/file will be
stored.

Passphrase + Salt       --> AES Key
E(Plaintext  + AES Key) --> Encrypted Text
Storage = Salt + Encrypted Text

Passphrase + Stored Salt    --> AES Key
D(Encrypted Text + AES Key) --> Output Text
Either text is decrypted or still encrypted. 

FUTURE CHANGES: Maybe allow to configure it so that we hash any
length passphrase to a desirable length/AES cipher type
i.e. Configure to always use AES-128, use passphrase to produce
a 16 byte hash digest.
'''
# Create some random salt of 128 bits or 16 bytes
salt = os.urandom(16)
iterations = 10000
key_size = 16
aes_key = hashlib.pbkdf2_hmac("sha256", PASS.encode(), salt, 1024, key_size)
# New AES_key from pass and random salt
print(binascii.hexlify(aes_key))

# Encrypt plaintext using that AES key
plaintext = MESSAGE.encode()
encCipher = AES.new(aes_key, AES.MODE_ECB)
# Pad the text to be multiples of 16
paddedPlain = pad(plaintext, 16)
cipherText = encCipher.encrypt(paddedPlain)
print("My Plaintext Message:", MESSAGE)
print("Encrypted Plaintext :", end=" ")
print(cipherText)

# Store the salt and encrypted file name