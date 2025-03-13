# FilecryptionCC
## Journal Through Development
### 02/26/2025
The first goal of making this program was to successfully encrypt a file from the command line. This could be done with any symmetric encryption type. The purpose of this is to be able to achieve taking commands from the CL and translate them into something meaningful in the main file; filecryption.py. 

Additionally, by starting off with a simple task as this, I can also begin to slowly learn and implement a simple GUI using PyQt.

### 03/05/2025
When looking back at my code, I realized that I didn't start small enough. Much of how the user needs to interact with the script via the command line did not make much sense and will simply make it more difficult for me to implement a GUI for the future. It also made it more confusing for the user to use.

No progress was being made so I have to unfortunately break everything down and essentially start from scratch while only keeping some elements of the  original code I started writing out.

## Improvements
### 03/05/2025
- Encryption mode changed from ECB to CBC for a stronger encryption
- Command line usage simplified to `python3 filecryption.py <message>`
- Moved script down to proper section
- Changed from using AES-128 to AES-256 as default to be quantum resistant

### 03/06/2025
- Included getpass library so that characters when entering password stays hidden
- IV now gets generated via the `.pbkdf2_hmac` function under `generate_key_and_iv`
	- A longer key is generated; 32 bytes --> 48 bytes
	- First 32 bytes = key, last 16 bytes = iv
- Began adding feature to encrypt files only using file types that Python can natively open/read

### 03/12/2025
- Included a warning to users if their ".enc" file was found and gives them the option to overwrite or keep
- Decrypting .enc files decrypted succesfully!!!