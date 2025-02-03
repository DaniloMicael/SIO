import time
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


# ---------------- HYBRID ENCRYPTION ---------------- #


def hybrid_encrypt(file_name, pub_key_file, aes_key_file, output_file="hybrid_encrypted_file.bin"):
    # Load public key
    with open(pub_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    # Generate a random AES key (128-bit) and IV
    aes_key = os.urandom(16)
    iv = os.urandom(16)

    # Encrypt the file using AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = sym_padding.PKCS7(128).padder()

    start_time = time.time()
    with open(file_name, 'rb') as f, open(output_file, 'wb') as encrypted_file:
        encrypted_file.write(iv)            # Write IV to the file
        while chunk := f.read(64 * 1024):   # Read in chunks for large files
            padded_chunk = padder.update(chunk)
            encrypted_file.write(encryptor.update(padded_chunk))
        encrypted_last_chunk = encryptor.update(padder.finalize())
        encrypted_file.write(encrypted_last_chunk + encryptor.finalize())
    encryption_time = time.time() - start_time

    # Encrypt the AES key with RSA using OAEP padding for randomness
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Write the encrypted AES key to a separate file
    with open(aes_key_file, "wb") as key_file:
        key_file.write(encrypted_aes_key)

    print(f"File encrypted successfully in {encryption_time:.2f}s")
    print(f"AES key encrypted and saved as {aes_key_file}.")
    
    
# ---------------- HYBRID DECRYPTION ---------------- #  
    

def hybrid_decrypt(file_name, priv_key_file, key_file, output_file="decrypted_file.txt"):
    # Load private key
    with open(priv_key_file, "rb") as key_file_obj:
        private_key = serialization.load_pem_private_key(key_file_obj.read(), password=None)

    # Load the encrypted AES key
    with open(key_file, "rb") as key_file_obj:
        encrypted_aes_key = key_file_obj.read()

    # Decrypt the AES key with RSA
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt the file using AES
    start_time = time.time()
    with open(file_name, 'rb') as encrypted_file, open(output_file, 'wb') as decrypted_file:
        iv = encrypted_file.read(16)  # Read the IV
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        unpadder = sym_padding.PKCS7(128).unpadder()

        while chunk := encrypted_file.read(64 * 1024):
            decrypted_chunk = decryptor.update(chunk)
            unpadded_chunk = unpadder.update(decrypted_chunk)
            decrypted_file.write(unpadded_chunk)
        decrypted_file.write(unpadder.update(decryptor.finalize()) + unpadder.finalize())

    decryption_time = time.time() - start_time
    print(f"File decrypted successfully in {decryption_time:.2f}s")


# ---------------- MAIN ---------------- #


if __name__ == "__main__":
    # Hardcoded file paths and RSA key file paths
    large_file = "large_file_500mb.txt"
    aes_key_file = "encrypted_aes_key.bin"
    rsa_pub_key_file = "rsa_public_key.pem"
    rsa_priv_key_file = "rsa_private_key.pem"

    # Generate RSA keys (once, or use pre-existing ones)
    rsa_key_size = 2048  # Use 2048-bit keys for stronger encryption
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=rsa_key_size)
    public_key = private_key.public_key()

    # Save the RSA keys to files
    with open(rsa_pub_key_file, "wb") as f:
        f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                        format=serialization.PublicFormat.SubjectPublicKeyInfo))

    with open(rsa_priv_key_file, "wb") as f:
        f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                          format=serialization.PrivateFormat.PKCS8,
                                          encryption_algorithm=serialization.NoEncryption()))

    # Run the hybrid encryption
    print("\nHybrid Encryption Benchmark:")
    hybrid_encrypt(large_file, rsa_pub_key_file, aes_key_file)

    # Run the hybrid decryption
    print("\nHybrid Decryption Benchmark:")
    hybrid_decrypt("hybrid_encrypted_file.bin", rsa_priv_key_file, aes_key_file)
