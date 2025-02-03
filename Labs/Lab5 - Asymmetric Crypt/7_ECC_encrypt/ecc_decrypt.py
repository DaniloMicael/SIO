import sys
import json
import base64
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


# Load the private key of the receiver from file
def load_private_key(serialized_priv_key_file, password):
    with open(serialized_priv_key_file, "rb") as key_file:
        serialized_private_key = key_file.read()
    private_key = serialization.load_pem_private_key(
        serialized_private_key,
        password=password.encode(),
    )      
    return private_key


# Generate AES key using ECDH shared secret, so it can be used to encrypt/decrypt the data
def derive_aes_key(shared_secret):
    key_derivation_function = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'ECC_AES_Key_Derivation'
    )
    key = key_derivation_function.derive(shared_secret)
    return key


def aes_decrypt(key, plaintext):
    hash_instance = hashes.Hash(hashes.SHA256())
    hash_instance.update(key)
    iv = hash_instance.finalize()[:16]  # IV derived from the key ([0:16] means the first 16 bytes, because the IV is 16 bytes long and the hash is 32 bytes long)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(plaintext) + decryptor.finalize()
    return decrypted_data


if __name__ == "__main__":
    receiver_priv_key_file = sys.argv[1]
    password = sys.argv[2]
    private_key = load_private_key(receiver_priv_key_file, password)

    # Read the input from stdin (the encrypted JSON)
    encrypted_input = json.loads(sys.stdin.read())

    # Decode the ephemeral public key
    ephemeral_pub_key_bytes = base64.b64decode(encrypted_input['ephemeral_public_key'])
    ephemeral_public_key = serialization.load_pem_public_key(ephemeral_pub_key_bytes)

    # Compute shared secret
    shared_secret = private_key.exchange(ec.ECDH(), ephemeral_public_key)
    aes_key = derive_aes_key(shared_secret)

    # Decode and decrypt the ciphertext
    ciphertext = base64.b64decode(encrypted_input['ciphertext'])
    plaintext = aes_decrypt(aes_key, ciphertext)

    # Print the decrypted plaintext to standard output
    sys.stdout.write(plaintext.decode())
