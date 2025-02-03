Ensure you have the `cryptography` library installed:

```bash
pip install cryptography
```

### What is `Serialization`?

- **Serialization** is the process of converting an object into a format that can be easily stored or transmitted (remember Carlos Costa explaining the serialization of Java objects into byte streams, so they can be saved to disk or sent over a network, to be later deserialized back into objects and reused).
- In the **context of cryptography**, serialization is used to convert cryptographic keys into a `format that can be saved to a file or transmitted over a network`. 
- This **allows keys to be stored persistently** and shared between different systems.
- The `cryptography` library provides functions to serialize and deserialize cryptographic keys.
- In this exercise, we will generate an RSA key pair and serialize the public and private keys to files with the `.pem` extension (PEM format).
- PEM format is recognizable by the distinctive -----BEGIN {format}----- and -----END {format}----- markers that enclose the key data.


### How to Run the Program:

1. Save the program as `rsa_keygen.py`.
2. Run it from the command line and specify the key file names and the key size (1024, 2048, 3072, or 4096 bits), for example:

```bash
time python3 1_RSA_key_pair_gen/rsa_keygen.py pub.pem priv.pem 4096
```

The `time` command will measure how long it takes for the program to run.

### Example Usage:

```bash
$ time python3 1_RSA_key_pair_gen/rsa_keygen.py pub.pem priv.pem 2048

RSA key pair generated in 0.12 seconds

real    0m0.219s
user    0m0.206s
sys     0m0.013s
```

### Questions:

1. **What do you think of using 4096-bit keys by default in relation to speed?**
   - **4096-bit keys** offer stronger security but are slower to generate and slower for cryptographic operations compared to smaller keys like 2048-bit or 3072-bit. Using 4096-bit keys by default can slow down systems, especially when handling many operations, but it does increase the security against modern attacks. For general-purpose applications, 2048-bit keys are often recommended for a balance between security and performance. However, for long-term security, 4096-bit keys may be more appropriate despite the performance hit.

2. **How does the actual key size vary with the number of bits?**
   - The actual key size increases proportionally to the number of bits. For example, a 2048-bit key is twice as long as a 1024-bit key, and a 4096-bit key is twice as long as a 2048-bit key. However, the **time complexity** for key generation and cryptographic operations increases **non-linearly**. Larger keys take disproportionately longer to generate and use, **as the algorithms involve modular exponentiation**, which becomes more expensive as the key size grows.

### Experiment:

You can run the program several times with different key sizes and use the `time` output to compare the performance differences. For example:

```bash
time python3 1_RSA_key_pair_gen/rsa_keygen.py pub.pem priv.pem 1024
time python3 1_RSA_key_pair_gen/rsa_keygen.py pub.pem priv.pem 2048
time python3 1_RSA_key_pair_gen/rsa_keygen.py pub.pem priv.pem 3072
time python3 1_RSA_key_pair_gen/rsa_keygen.py pub.pem priv.pem 4096
```

Record the elapsed time and compare how the key generation time scales with the key size.