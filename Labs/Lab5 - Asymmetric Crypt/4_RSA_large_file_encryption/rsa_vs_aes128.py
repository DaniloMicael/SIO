import time
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import os


# ---------------- RSA ENCRYPTION/DECRYPTION ---------------- #

def rsa_encrypt_decrypt_benchmark(file_name, pub_key_file, priv_key_file, chunk_size):  # Adjust for RSA 1024
    encrypted_chunks = []
    
    # Load public key
    with open(pub_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    # Load private key
    with open(priv_key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    # Encrypt the file in chunks
    start_time = time.time()
    with open(file_name, 'rb') as f:
        while chunk := f.read(chunk_size):
            encrypted_chunk = public_key.encrypt(chunk, padding.PKCS1v15())
            encrypted_chunks.append(encrypted_chunk)
    encryption_time = time.time() - start_time

    # Decrypt the chunks
    decrypted_data = b""
    start_time = time.time()
    for encrypted_chunk in encrypted_chunks:
        decrypted_data += private_key.decrypt(encrypted_chunk, padding.PKCS1v15())
    decryption_time = time.time() - start_time

    return encryption_time, decryption_time

# ---------------- AES ENCRYPTION/DECRYPTION ---------------- #

def aes_encrypt_decrypt_benchmark(file_name):
    # Load file data
    with open(file_name, 'rb') as f:
        data = f.read()

    # Generate random 128-bit key and IV
    key = os.urandom(16)
    iv = os.urandom(16)

    # Pad data to align with AES block size
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    start_time = time.time()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    encryption_time = time.time() - start_time

    # Decrypt data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    start_time = time.time()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decryption_time = time.time() - start_time

    # Unpad decrypted data
    unpadder = sym_padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return encryption_time, decryption_time

# ---------------- RUN BENCHMARK ---------------- #

if __name__ == "__main__":
    # File paths and RSA key sizes
    file_100kb = "file_100kb.txt"
    file_10mb = "file_10mb.txt"
    rsa_pub_key_file = "rsa_public_key.pem"
    rsa_priv_key_file = "rsa_private_key.pem"
    rsa_key_size = 1024

    # Generate RSA keys
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=rsa_key_size)
    public_key = private_key.public_key()

    # Save the keys to files
    with open(rsa_pub_key_file, "wb") as f:
        f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PublicFormat.SubjectPublicKeyInfo))

    with open(rsa_priv_key_file, "wb") as f:
        f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                          format=serialization.PrivateFormat.PKCS8,
                                          encryption_algorithm=serialization.NoEncryption()))

    # Run benchmarks for RSA
    print("\nRSA 1024-bit Benchmark:")
    for file in [file_100kb, file_10mb]:
        rsa_enc_time, rsa_dec_time = rsa_encrypt_decrypt_benchmark(file, rsa_pub_key_file, rsa_priv_key_file, rsa_key_size // 8 - 11)
        print(f"File: {file} - Encryption time: {rsa_enc_time:.2f}s, Decryption time: {rsa_dec_time:.2f}s")

    # Run benchmarks for AES
    print("\nAES 128-bit Benchmark:")
    for file in [file_100kb, file_10mb]:
        aes_enc_time, aes_dec_time = aes_encrypt_decrypt_benchmark(file)
        print(f"File: {file} - Encryption time: {aes_enc_time:.2f}s, Decryption time: {aes_dec_time:.2f}s")
