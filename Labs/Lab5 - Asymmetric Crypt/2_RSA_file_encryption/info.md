Here’s a Python program that uses the RSA algorithm to encrypt a file. The program allows the user to provide the original file name to encrypt, the public key file, and the name for the encrypted output file. The RSA encryption will use **PKCS #1 v1.5 padding** (which is considered insecure for new applications but is implemented here as requested). OAEP is the recommended padding scheme for modern applications.

We will use the `cryptography` library for this, as it supports RSA encryption and the necessary padding schemes. To handle the size limitation of RSA (where the input size must be less than the key size minus padding), the program will split the input file into chunks that fit within the allowed block size.

### Python Code for RSA Encryption (`rsa_encrypt.py`)

### How to Run the Program

1. Save the above program as `rsa_encrypt.py`.
2. Use the following command to encrypt a file:

```bash
python 2_RSA_file_encryption/rsa_encrypt.py <original_file> <public_key_file> <encrypted_file>
```

For example:

```bash
python 2_RSA_file_encryption/rsa_encrypt.py file.txt pub.pem encrypted_file.bin
```

### Explanation

1. **Loading the Public Key**: The program reads the public key from the provided PEM file using the `cryptography` library. The public key is needed to perform RSA encryption.
   
2. **Block Size Calculation**: The block size is calculated as the size of the RSA key (in bytes) minus 11 bytes, which is required for the **PKCS #1 v1.5 padding**. For example:
   - For a 1024-bit key (128 bytes), the block size will be 128 - 11 = 117 bytes.
   - For a 2048-bit key (256 bytes), the block size will be 256 - 11 = 245 bytes.

3. **Reading and Encrypting in Chunks**: The program reads the original file in chunks equal to the calculated block size. It then encrypts each chunk using the RSA public key and writes the encrypted chunk to the output file.

4. **Encryption**: The RSA encryption is done using the `encrypt` function with the public key and PKCS #1 v1.5 padding.


### Notes:
- **File Size Limitation**: RSA is not designed to encrypt large data directly due to the block size limitations. This program handles this by encrypting the file in chunks, but for larger files or modern applications, you would typically encrypt the data with a symmetric cipher (like AES) and encrypt the symmetric key with RSA (known as hybrid encryption).
  
- **PKCS #1 v1.5 Padding**: This padding scheme has known vulnerabilities, such as the Bleichenbacher attack. It’s used here per your request, but in modern applications, **OAEP** padding (Optimal Asymmetric Encryption Padding) is recommended for RSA encryption.

### Testing:
After running the encryption, you can test decrypting the file with the corresponding private key (using a similar program for RSA decryption) to verify that the encryption was successful. Let me know if you'd like help with that part too!