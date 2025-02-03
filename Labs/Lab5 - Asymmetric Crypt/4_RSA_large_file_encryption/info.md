As should be known by now, RSA encryption is not efficient and is not recommended to encrypt data bigger than its block size.

## Symmetric vs. Asymmetric cryptography benchmark
Generate two files with 100 kB and 10 MB of size. Using these files and the time application, register the time it takes to encrypt and decrypt these files with RSA (key = 1024 bits) and AES128. 

To create a cryptographic benchmark comparing symmetric (AES) and asymmetric (RSA) encryption using your existing Python code, follow these steps:

### Step 1: Generate Test Files
Use the `dd` command to generate files of the required sizes.

```bash
# Generate a 100 kB file
dd if=/dev/zero of=file_100kb.txt bs=1024 count=100

# Generate a 10 MB file
dd if=/dev/zero of=file_10mb.txt bs=1048576 count=10
```

### Step 2: Modify Your Python Code for Benchmarking
Create a new Python script to measure the time taken for encryption and decryption using both RSA and AES.

### Step 3: Run the Benchmark
Execute the benchmark script to measure the encryption and decryption times.

```bash
python3 benchmark_script.py
```

## RESULTS - Benchmark Summary

```bash
RSA 1024-bit Benchmark:
File: file_100kb.txt - Encryption time: 0.01s, Decryption time: 0.09s
File: file_10mb.txt - Encryption time: 0.75s, Decryption time: 199.94s

AES 128-bit Benchmark:
File: file_100kb.txt - Encryption time: 0.00s, Decryption time: 0.00s
File: file_10mb.txt - Encryption time: 0.02s, Decryption time: 0.02s
```

| File Size | Algorithm | Operation | Time (s) |
|-----------|-----------|-----------|----------|
| 100 kB    | RSA 1024  | Encrypt   | 0.01     |
| 100 kB    | RSA 1024  | Decrypt   | 0.09     |
| 100 kB    | AES 128   | Encrypt   | 0.00     |
| 100 kB    | AES 128   | Decrypt   | 0.00     |
| 10 MB     | RSA 1024  | Encrypt   | 0.75     |
| 10 MB     | RSA 1024  | Decrypt   | 199.94   |
| 10 MB     | AES 128   | Encrypt   | 0.02     |
| 10 MB     | AES 128   | Decrypt   | 0.02     |


Those benchmark results show a significant difference between RSA and AES performance, especially with larger file sizes, highlighting how much more efficient symmetric encryption (AES) is for large data compared to asymmetric encryption (RSA). 

