import sys
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# This sample demonstrates how to generate a private key, how to serialize it WITH A PASSWORD and how to generate the corresponding public key
def generate_ecc_key_pair(password, curve_instance):
    
    # Generate a random private key for the curve instance
    private_key = ec.generate_private_key(curve_instance) # This is a 521-bit random integer
    
    # From that private key, we generate the public key
    public_key = private_key.public_key()
    
    # Serialize private key with password protection
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
    )
    # You can also serialize the key without a password, by relying on NoEncryption.
    
    # The public key is serialized as follows:
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return pem_private_key, pem_public_key

# Main function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ecc_keygen.py <password>")
        sys.exit(1)
    
    # First, choose a curve
    curve_instance = ec.SECP521R1()
    password = sys.argv[1].strip()

    # Generate the key pair
    private_key, public_key = generate_ecc_key_pair(password, curve_instance)

    # Save both keys in a single file
    with open("KPair.pem", "wb") as f:
        f.write(private_key)
        f.write(public_key)

    print("ECC key pair generated and saved to KPair.pem.")
