import sys
import json
import base64
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


# Load the public key of the receiver from file
def load_public_key(serialized_pub_key_file):
    with open(serialized_pub_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key


# Generate AES key using ECDH shared secret, so it can be used to encrypt/decrypt the data
def derive_aes_key(shared_secret):
    # For most applications the shared_key should be passed to a key derivation function. 
    # This allows mixing of additional information into the key, derivation of multiple keys, and destroys any structure that may be present.
    key_derivation_function = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'ECC_AES_Key_Derivation'
    )
    key = key_derivation_function.derive(shared_secret)
    return key


# For symmetric encryption, you can use AES in CTR mode and an IV derived from the secret key (e.g., by hashing it).
def aes_encrypt(key, plaintext):
    # SHA-256 is a cryptographic hash function from the SHA-2 family and is standardized by NIST. It produces a 256-bit message digest.
    # Create a SHA-256 hash instance
    hash_instance = hashes.Hash(hashes.SHA256())
    hash_instance.update(key)
    iv = hash_instance.finalize()[:16]  # IV derived from the key ([0:16] means the first 16 bytes, because the IV is 16 bytes long and the hash is 32 bytes long)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(plaintext) + encryptor.finalize()
    return encrypted_data


if __name__ == "__main__":
    receiver_pub_key_file = sys.argv[1]
    # Deserialize the public key of the receiver
    receiver_public_key = load_public_key(receiver_pub_key_file)
    
    # Choose a curve
    curve_instance = ec.SECP521R1()

    # Generate ephemeral private/public key pair for ECDH, so that the shared secret can be computed
    ephemeral_private_key = ec.generate_private_key(curve_instance)
    ephemeral_public_key = ephemeral_private_key.public_key()

    # Compute shared secret
    shared_secret = ephemeral_private_key.exchange(ec.ECDH(), receiver_public_key)
    # Derive AES key from shared secret
    aes_key = derive_aes_key(shared_secret)

    # Read input data from stdin and encrypt
    plaintext = sys.stdin.read().encode()
    ciphertext = aes_encrypt(aes_key, plaintext)

    # Serialize ephemeral public key, so that it can be sent to the receiver (converted to PEM)
    serialized_ephemeral_pub_key = ephemeral_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Encode the ephemeral public key
    encoded_serialized_ephemeral_pub_key = base64.b64encode(serialized_ephemeral_pub_key).decode()

    # Encode the ciphertext
    encoded_ciphertext = base64.b64encode(ciphertext).decode()

    # Prepare JSON output
    result = {
        'ephemeral_public_key': encoded_serialized_ephemeral_pub_key,
        'ciphertext': encoded_ciphertext
    }

    # Print to standard output formatted 
    print(json.dumps(result, indent=4))
