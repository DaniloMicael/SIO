To generate an ECC key pair using the P-521 (prime number, o 'q' em  "nG mod q") curve and save it in a file while protecting the private key with a password, you can use the `cryptography` library in Python. Below is a sample implementation for the program `ecc_keygen.py` that meets your requirements: (see `ecc_keygen.py`)

### How to Run the Program
1. Ensure you have the `cryptography` library installed:

2. Save the above code in a file named `ecc_keygen.py`.

3. Run the program with a password parameter:
   ```bash
   python3 ecc_keygen.py your_password
   ```

4. This will generate an ECC key pair using the P-521 curve, and both keys will be saved in a file named `KPair.pem`. The private key will be encrypted with the provided password. 

### Notes
- The program uses the `SECP521R1` curve as specified.
- It saves both keys in PEM format, which is a common format for storing cryptographic keys.
- The private key is protected using a password-based encryption scheme (PBKDF2).
- You can change the curve by modifying the `ec.SECP521R1()` parameter if needed.