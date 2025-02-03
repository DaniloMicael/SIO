import sys
import time
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def write_private_key(private_key, filename):
    # If you have a private key, you can use private_bytes() to serialize the key.
    key_pem = private_key.private_bytes(                    # "private_bytes" method is used to serialize the private key
        encoding=serialization.Encoding.PEM,                # PEM is a text format for encoding keys
        format=serialization.PrivateFormat.PKCS8,           # PKCS8 is a standard for encoding private
        encryption_algorithm=serialization.NoEncryption()   # No encryption is used for the private key serialization (in the file, the key data is not encrypted, it is in plain text)
    )
    # Serialized keys may optionally be encrypted on disk using a password. 
    # In this example we loaded an unencrypted key.
    
    with open(filename, "wb") as key_file:
        key_file.write(key_pem)
        
        
def write_public_key(public_key, filename):
    # For public keys you can use public_bytes() to serialize the key.
    # public_key = private_key.public_key() # Extract the public key from the private key
    key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo # SubjectPublicKeyInfo is a standard for encoding public keys
    )
    
    with open(filename, "wb") as key_file:
        key_file.write(key_pem)


def generate_rsa_key_pair(pub_filename, priv_filename, k_size):
    
    # Generate the private key
    private_key = rsa.generate_private_key(
        public_exponent=65537, # 2^16 + 1, is used to speed up encryption and decryption    
        key_size=k_size
    )

    # Extract the public key from the private key
    public_key = private_key.public_key()

    # Save the private key in PEM format
    write_private_key(private_key, priv_filename)

    # Save the public key in PEM format
    write_public_key(public_key, pub_filename)
    

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 keygen.py <public_key_file> <private_key_file> <key_size>")
        sys.exit(1)

    pub_filename = sys.argv[1]
    priv_filename = sys.argv[2]
    key_size = int(sys.argv[3])

    start_time = time.time()
    generate_rsa_key_pair(pub_filename, priv_filename, key_size)
    end_time = time.time()

    print(f"RSA key pair generated in {end_time - start_time:.2f} seconds")
