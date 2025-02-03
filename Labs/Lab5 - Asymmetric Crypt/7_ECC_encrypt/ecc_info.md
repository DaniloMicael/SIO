# ECC Quick Reference

## Key Generation

```python
# Choose a curve and initialize the key pair generator (curve instance)
curve_instance = ec.SECP521R1()

# Generate a private key
private_key = ec.generate_private_key(curve_instance)
# Get the public key from the private key
public_key = private_key.public_key()

# Save the keys to files, e.g., PEM format
# For that, we need to serialize the keys (converting them to bytes)
# Serialize private key with password protection
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'password')
)
# You can also serialize the key without a password, by relying on NoEncryption.

pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
```

## Key Loading

```python
# Load the keys from files

# Load the private key
with open("private_key.pem", "rb") as key_file:
    pem_private_key = key_file.read()

private_key = serialization.load_pem_private_key(
    pem_private_key,
    password=b'password'
)

# Load the public key
with open("public_key.pem", "rb") as key_file:
    pem_public_key = key_file.read()

public_key = serialization.load_pem_public_key(
    pem_public_key_file
)
```

## Key Exchange Algorithm (ECDH)

The `Elliptic Curve Diffie-Hellman` Key Exchange algorithm standardized in NIST publication 800-56A.

For most applications the `shared_key` should be passed to a `key derivation function`. This allows mixing of additional information into the key, derivation of multiple keys, and destroys any structure that may be present.

Note that while elliptic curve keys can be used for both signing and key exchange,` this is bad cryptographic practice`. Instead, users should generate separate signing and ECDH keys.

**`ECDHE` (or EECDH), the `ephemeral` form of this exchange, is strongly preferred over simple ECDH and provides forward secrecy when used.** 
You must **`generate a new private key using generate_private_key() for each exchange()`** when performing an ECDHE key exchange. An example of the ephemeral form:

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

curve = ec.SECP384R1()

# Generate a private key for use in the exchange.
private_key = ec.generate_private_key(curve)

# In a real handshake the peer_public_key will be received from the
# other party. For this example we'll generate another private key
# and get a public key from that.
# In the real world you would have already exchanged the public keys.
# In the last exercice of the practical, the public key provided in a file.
peer_public_key = ec.generate_private_key(curve).public_key() # file.read()

# Perform the key exchange and generate the shared key (secret).
shared_key = private_key.exchange(ec.ECDH(), peer_public_key)

# Perform key derivation.
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key)

# For the next handshake we MUST generate another private key. !!!!!!!!!!!
private_key_2 = ec.generate_private_key(curve)

peer_public_key_2 = ec.generate_private_key(curve).public_key()

shared_key_2 = private_key_2.exchange(ec.ECDH(), peer_public_key_2)

derived_key_2 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key_2)
```