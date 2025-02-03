import sys
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


def load_public_key(pub_key_file):
    """Load public key from a PEM file."""
    # If you already have an on-disk key in the PEM format (which are recognizable by the distinctive 
    # -----BEGIN {format}----- and -----END {format}----- markers), you can load it:
    with open(pub_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key


def rsa_encrypt_file(original_file, pub_key_file, encrypted_file, block_size):
    """Encrypt a file using RSA with PKCS #1 v1.5 padding."""
    public_key = load_public_key(pub_key_file)

    # RSA encryption is interesting because encryption is performed using the public key, meaning anyone can encrypt data. 
    # The data is then decrypted using the private key.

    # Like signatures, RSA supports encryption with several different padding options. 
    # Here’s an example using PKCS1 v1.5 padding:
    # PKCS1 v1.5 (also known as simply PKCS1) is a simple padding scheme developed for use with RSA keys. 
    # This padding can be used for signing and encryption.
    # It is not recommended that PKCS1v15 be used for new applications, as it is vulnerable to several attacks.
    # We also could use OAEP padding, and PSS signing.
    with open(original_file, "rb") as f_in, open(encrypted_file, "wb") as f_out:
        # Read the input file in chunks based on the block size (key size - padding overhead)
        while True:
            chunk = f_in.read(block_size)
            if not chunk:
                break

            # Encrypt the chunk using RSA
            encrypted_chunk = public_key.encrypt( # (method) encrypt: Any | ((plaintext: bytes, padding: AsymmetricPadding) -> bytes)
                chunk,
                padding.PKCS1v15()
            )

            # Write the encrypted chunk to the output file
            f_out.write(encrypted_chunk)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python rsa_encrypt.py <original_file> <public_key_file> <encrypted_file>")
        sys.exit(1)

    original_file = sys.argv[1]
    pub_key_file = sys.argv[2]
    encrypted_file = sys.argv[3]

    # Get the public key size from the key file
    public_key = load_public_key(pub_key_file)
    
    # Convert number of bits to number of bytes
    key_size = public_key.key_size // 8         

    # Calculate block size (Using the PKCS #1 default configuration, the block size is equal to the key size minus eleven bytes (eleven bytes for padding). 
    # So, for example using a 1024 bits RSA key (128 bytes), the block size is 117 bytes (128 - 11).)
    # Note that this scheme is not recommended for new applications.
    block_size = key_size - 11
    # PKCS#1 is a standard (states how thisng should be done) for public key encryption and decryption that is defined in the RSA Labs PKCS#1 standard.
    # And it defines, among other things, padding schemes for RSA encryption and decryption.
    # The padding schemes are used to ensure that the input data is the same size as the RSA key.
    # Padding is used to add random bytes to the input data to make it the same size as the RSA key and also to make it more secure, randomizing the input data.
    
    # Perform encryption
    rsa_encrypt_file(original_file, pub_key_file, encrypted_file, block_size)

    print(f"File '{original_file}' encrypted and saved as '{encrypted_file}'")
    
