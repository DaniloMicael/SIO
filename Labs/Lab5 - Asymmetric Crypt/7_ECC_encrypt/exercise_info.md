### ECC_encrypt Program

1. **Generates an ephemeral key pair for encryption.**
2. **Uses the receiver’s public key to compute a shared secret.**
3. **Derives an AES key from the shared secret.**
4. **Encrypts the input using AES in CTR mode.**
5. **Outputs the ciphertext along with the originator’s public key.**

### ECC_decrypt Program

1. **Reads the encrypted data and the sender’s public key.**
2. **Uses the receiver’s private key to compute the shared secret.**
3. **Derives the AES key from the shared secret.**
4. **Decrypts the input and outputs the plaintext.**

Let's implement these two programs.

#### ECC_encrypt Program

(See `ecc_encrypt.py`)

#### ECC_decrypt Program

(See `ecc_decrypt.py`)

### Explanation:
- **`ECC_encrypt`** takes the public key of the receiver, generates an ephemeral key pair, derives a shared secret, creates a symmetric AES key, and encrypts the plaintext.
- **`ECC_decrypt`** reads the ciphertext and ephemeral public key, computes the shared secret with the receiver's private key, derives the AES key, and decrypts the ciphertext.

### Usage:
```bash
# Encrypt
python ecc_encrypt.py recv_pub.pem < plaintext.txt > ciphertext.json

# Decrypt
python ecc_decrypt.py recv_priv.pem 1234 < ciphertext.json > recovered_plaintext.txt
```

This ensures that the encrypted message can only be decrypted by the holder of the private key corresponding to the receiver's public key.


## Explanation

This exercise focused on simulated a safe communication between two parties using ECC encryption. 
The sender encrypts a message using the receiver's public key ("ecc_encrypt.py"), and the receiver decrypts it using his own private key ("ecc_decrypt.py"). 
The shared secret is derived from the key exchange, and the message is encrypted and decrypted using AES in CTR mode, in both parties.


These two programs together implement an asymmetric encryption and decryption system using Elliptic Curve Cryptography (ECC) for key exchange and AES (Advanced Encryption Standard) for symmetric data encryption. 
Here's a detailed breakdown:

### **General Overview**
- **ECC** is used for secure key exchange through the Elliptic Curve Diffie-Hellman (ECDH) algorithm. ECC provides strong security with smaller key sizes, making it efficient and secure.
- **AES in CTR mode** is used for encrypting and decrypting data symmetrically once a shared secret is derived from the ECDH key exchange.
- **Python's `cryptography` library** is utilized for cryptographic operations.

### **Program 1: Sender's side ECC Encryption (`ecc_encrypt.py`)**
1. **Load the Receiver's Public Key:**
   - The public key is loaded from a PEM-encoded file to encrypt data for a specific recipient.
2. **Ephemeral Key Generation:**
   - A temporary (ephemeral) ECC private-public key pair is created for one-time use in this session.
3. **Shared Secret Computation:**
   - The ephemeral private key and the receiver's public key are used in the ECDH algorithm to compute a shared secret.
4. **Key Derivation:**
   - The shared secret is processed through the HKDF (HMAC-based Extract-and-Expand Key Derivation Function) to derive a 256-bit AES encryption key.
5. **Symmetric Encryption:**
   - The plaintext input is read from `stdin`, and the derived AES key is used to encrypt the data in **CTR (Counter) mode** with an IV derived from the AES key.
6. **Output Serialization:**
   - The ephemeral public key is serialized to PEM format and encoded in base64 for transmission.
   - The ciphertext is also base64-encoded.
   - The encrypted output is formatted as a JSON object containing the ephemeral public key and ciphertext.

### **Program 2: Receiver's side ECC Decryption (`ecc_decrypt.py`)**
1. **Load the Receiver's Private Key:**
   - The receiver's private key is loaded from a PEM-encoded file, with password protection for decryption.
2. **Read Encrypted Input:**
   - The program reads a JSON object containing the base64-encoded ephemeral public key and ciphertext from `stdin`.
3. **Ephemeral Public Key Deserialization:**
   - The ephemeral public key is decoded from base64 and deserialized.
4. **Shared Secret Computation:**
   - The receiver's private key and the ephemeral public key are used in ECDH to reconstruct the shared secret.
5. **Key Derivation:**
   - The shared secret is processed with HKDF to derive the AES decryption key.
6. **Symmetric Decryption:**
   - The ciphertext is decoded from base64 and decrypted using AES in CTR mode.
7. **Output:**
   - The decrypted plaintext is printed to `stdout`.

### **Essence and Workflow:**
- **Asymmetric Part (ECC):** The key exchange ensures that the encryption/decryption keys are shared securely without transmitting sensitive key material directly.
- **Symmetric Part (AES):** Once the shared secret is established, the data is encrypted using AES, which is more efficient for larger data volumes.
- **Security Highlights:**
  - **Ephemeral Key Pair:** Provides forward secrecy, ensuring that if the session's private key is compromised, past communications remain secure.
  - **Key Derivation Function (HKDF):** Adds an extra layer of security by ensuring the derived AES key is uniform and secure, even if the shared secret has structure.

**Overall**, the programs demonstrate a robust and efficient hybrid encryption approach where ECC is used for secure key exchange and AES for actual data encryption, combining the strengths of both asymmetric and symmetric encryption.