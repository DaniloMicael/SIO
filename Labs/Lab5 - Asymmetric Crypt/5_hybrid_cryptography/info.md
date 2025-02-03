
### Generate Test Files
Use the `dd` command to generate files of the required sizes.

```bash
# Generate a 500 MB file (half a gigabyte)
dd if=/dev/urandom of=large_file_500mb.txt bs=1M count=500
```

## RESULTS - Benchmark Summary

```bash
Hybrid Encryption Benchmark:
File encrypted successfully in 0.78s
AES key encrypted and saved as encrypted_aes_key.bin.

Hybrid Decryption Benchmark:
File decrypted successfully in 0.54s
```

| File Size | Algorithm | Operation | Time (s) |
|-----------|-----------|-----------|----------|
| 100 kB    | RSA 1024  | Encrypt   | 0.01     |
| 100 kB    | RSA 1024  | Decrypt   | 0.09     |
| 100 kB    | AES 128   | Encrypt   | 0.00     |
| 100 kB    | AES 128   | Decrypt   | 0.00     |
|-----------|-----------|-----------|----------|
| 10 MB     | RSA 1024  | Encrypt   | 0.75     |
| 10 MB     | RSA 1024  | Decrypt   | 199.94   |
| 10 MB     | AES 128   | Encrypt   | 0.02     |
| 10 MB     | AES 128   | Decrypt   | 0.02     |
|-----------|-----------|-----------|----------|
| 500 MB    | Hybrid    | Encrypt   | 0.78     |
| 500 MB    | Hybrid    | Decrypt   | 0.54     |


### Answers to the Questions on Hybrid Cryptography

1. **With this method, what is sent to the destination?**
   - In the hybrid cryptography approach, two key components are sent to the destination:
     - **Encrypted File**: The main content, which is the large file, is encrypted using a symmetric encryption algorithm (e.g., AES). This encrypted file is what is transmitted to the recipient.
     - **Encrypted AES Key**: Along with the encrypted file, the randomly generated symmetric key (used for AES encryption) is also sent, but it is encrypted using the recipient's public key (RSA). This ensures that only the recipient, who possesses the corresponding private key, can decrypt the AES key and subsequently decrypt the file.

2. **Should we always send the public key?**
   - **No, we do not always send the public key.** 
     - The public key is typically shared beforehand through a secure channel, or it can be obtained from a trusted certificate authority (CA) or a public key infrastructure (PKI). The recipient's public key is used solely for the purpose of encrypting the AES key for secure transmission.
     - Sending the public key with each message is generally unnecessary and may introduce redundancy, as the public key should be known or accessible to the sender prior to the file transfer. However, in cases where the public key may not be known or may need to be verified (e.g., in a dynamic environment), it can be sent along with the encrypted content, but this is less common. The focus should be on ensuring that the public key used for encryption is authentic and corresponds to the intended recipient.

### Conclusions from Benchmark Summary

1. **Performance Comparison Between RSA and AES**:
   - **Speed**: The AES encryption and decryption times are significantly faster than RSA for both file sizes tested (100 kB and 10 MB). AES encryption for 100 kB is effectively instantaneous (0.00 s), while RSA takes 0.01 s to encrypt small files and 0.75 s for larger files. This highlights AES's efficiency in processing large amounts of data.
   - **RSA Decryption Time**: The RSA decryption time for the 10 MB file (199.94 s) is notably high compared to encryption time (0.75 s). This discrepancy suggests that RSA is not suited for decrypting large amounts of data directly and reinforces the need for hybrid encryption when dealing with larger files.

2. **Hybrid Encryption Efficiency**:
   - **Time Efficiency**: The hybrid approach combining AES for file encryption and RSA for encrypting the AES key offers a balanced solution. The 500 MB file was encrypted in 0.78 s and decrypted in 0.54 s, demonstrating that hybrid encryption can handle large files effectively without the overhead associated with direct RSA encryption.
   - **Scalability**: The ability to efficiently encrypt larger files (500 MB) using this hybrid model indicates that it scales well with file size, maintaining relatively low processing times compared to pure RSA encryption.

3. **Practicality of Hybrid Encryption**:
   - The hybrid model is practical and secure, leveraging the speed of symmetric encryption (AES) for bulk data and the security of asymmetric encryption (RSA) for key management. This method addresses the limitations of RSA regarding data size while ensuring that only the intended recipient can decrypt the data using their private key.
   - The results underscore the importance of using the right algorithm for the right task. AES excels at fast, bulk encryption, while RSA is used sparingly for key exchange due to its computational intensity.

4. **Real-World Application**: 
   - The benchmarks suggest that for applications requiring the transfer of large files securely, hybrid encryption is the best practice. It provides both speed and security, ensuring that sensitive data can be shared quickly without compromising confidentiality.

5. **Conclusion on RSA Limitations**: 
   - The significant difference in decryption time for the larger RSA-encrypted file indicates its impracticality for scenarios where quick access to large datasets is needed. This limitation reinforces the value of using hybrid encryption for modern secure communications.

Overall, the results validate the use of hybrid encryption as a robust and efficient method for secure file transmission, especially when dealing with large files.