# SecureVault- AES Based File Encryption System

SecureVault is a file encryption and decryption system that uses AES (Advanced Encryption Standard) to protect sensitive files.

The project is structured into multiple modules:

**User Authentication** – Users log in with a username and password via a simple Streamlit interface.

**File Encryption** – Users can upload files, which are encrypted using AES GCM mode. The encryption key is derived from the username using PBKDF2.

**File Decryption** – To decrypt a file, the user must upload it, and the username serves as the decryption key. If the username does not match or the file is altered, decryption fails.

This system ensures confidentiality and access control, making it ideal for securing personal or sensitive documents. 🚀
