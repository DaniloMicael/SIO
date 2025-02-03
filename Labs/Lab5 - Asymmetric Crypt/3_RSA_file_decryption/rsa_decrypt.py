import sys
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


def load_private_key(priv_key_file):
    """Load private key from a PEM file."""
    # Serialized keys may optionally be encrypted on disk using a password. 
    # In this example we loaded an unencrypted key, and therefore we did not 
    # provide a password. 
    # If the key is encrypted we can pass a bytes object as the password argument.
    
    with open(priv_key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    return private_key


def rsa_decrypt_file(encrypted_file, priv_key_file, decrypted_file, block_size):
    """Decrypt a file using RSA with PKCS #1 v1.5 padding."""
    
    # Once you have an encrypted message, it can be decrypted using the private key:
    private_key = load_private_key(priv_key_file)

    with open(encrypted_file, "rb") as f_in, open(decrypted_file, "wb") as f_out:
        # Read the encrypted file in chunks based on the block size (key size)
        while True:
            encrypted_chunk = f_in.read(block_size)
            if not encrypted_chunk:
                break

            # Decrypt the chunk using RSA
            decrypted_chunk = private_key.decrypt(
                encrypted_chunk,
                padding.PKCS1v15()
            )

            # Write the decrypted chunk to the output file
            f_out.write(decrypted_chunk)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python rsa_decrypt.py <encrypted_file> <private_key_file> <decrypted_file>")
        sys.exit(1)

    encrypted_file = sys.argv[1]
    priv_key_file = sys.argv[2]
    decrypted_file = sys.argv[3]

    # Get the private key size from the key file
    private_key = load_private_key(priv_key_file)
    key_size = private_key.key_size // 8            # Convert bits to bytes

    # Perform decryption
    rsa_decrypt_file(encrypted_file, priv_key_file, decrypted_file, key_size)

    print(f"File '{encrypted_file}' decrypted and saved as '{decrypted_file}'")
