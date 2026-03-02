# 🔐 Encrypted Chat Application

A secure client-server chat application with AES-256 encryption, built for my Cybersecurity Internship at Syntecxhub.

## 📋 Project Overview
This project implements a real-time encrypted chat system where all messages are secured using AES encryption before transmission. It demonstrates core cybersecurity concepts including symmetric encryption, secure key handling, and network programming.

## ✨ Features

### 🔒 Security Features
- **AES-256-CBC encryption** for all messages
- **Random Initialization Vectors (IV)** per message
- **Pre-shared key** authentication
- **Secure key hashing** with SHA-256
- **PKCS7 padding** for block alignment

### 💬 Chat Features
- **Multi-client support** with threading
- **Real-time message broadcasting**
- **User join/leave notifications**
- **Message history logging**
- **Graceful disconnection handling**

### 📊 Additional Tools
- **Chat history viewer** with encryption details
- **JSON report generator** with encrypted messages
- **Key exchange demonstration**

## 🛠️ Technologies Used
- **Python 3.11**
- **PyCryptodome** (AES encryption)
- **Socket Programming** (TCP)
- **Threading** (Concurrent clients)
- **Base64** (Data encoding)

## 📁 Project Structure
├── server.py # Multi-threaded chat server
├── client.py # Encrypted chat client
├── encryption.py # AES encryption/decryption module
├── key_exchange_demo.py # Key exchange demonstration
├── view_history.py # Chat history viewer tool
└── README.md # Project documentation

## 🚀 Installation & Setup

### Prerequisites
```bash
# Install required library
pip install pycryptodome

python server.py
Follow the prompts to configure:

Server IP (default: 127.0.0.1)

Port (default: 5555)

Pre-shared key (default: MySecretKey123!@#)

2. Start Clients
bash
# In separate terminal windows
python client.py
Use the same server details and key as the server.

📸 Usage Example
Server Output
text
🔐 ENCRYPTED CHAT SERVER STARTED
========================================
📡 Host: 127.0.0.1
🔌 Port: 5555
🔑 Pre-shared key: MySecretKey123!@#
📝 Log file: chat_log_20260302_152946.txt
========================================
Waiting for clients...

📞 New connection from 127.0.0.1:54321
✅ Alice connected
📨 [15:30] Alice: Hello everyone!
Client Output
text
Enter your name: Alice

✨ Welcome Alice! You're connected to encrypted chat.

Start chatting! (type 'quit' to exit)
You: Hello everyone!
[15:30] Bob: Hi Alice!
You:
🔒 How Encryption Works
Key Derivation: Pre-shared key → SHA-256 → 32-byte AES key

Encryption: Message + Random IV → AES-CBC → Base64

Decryption: Base64 → Extract IV → AES-CBC → Original message

Transmission: Only encrypted data travels over network

📝 Message Logging
All messages are automatically logged server-side:

text
[2026-03-02 15:30:22] Alice: Hello everyone!
[2026-03-02 15:30:25] Bob: Hi Alice!
[2026-03-02 15:30:28] SYSTEM: Bob joined
View Encrypted History
bash
python view_history.py
This tool lets you:

View chat history with encryption status

Generate JSON reports with encrypted messages

Save encrypted-only versions of chats

🎯 Project Requirements Met
✅ AES encryption on messages

✅ Socket communication (TCP)

✅ Key exchange handling (pre-shared + demo)

✅ Safe IV usage (random per message)

✅ Multiple clients (threading)

✅ Message logging

✅ Error handling

✅ Basic UI (colored terminal output)

⚠️ Security Notes
This is for educational purposes

In production, use proper key exchange (RSA/Diffie-Hellman)

Add certificate validation for production use

Consider using authenticated encryption (GCM mode)

📊 Sample Chat History Report
The history viewer can generate JSON reports:

json
{
  "timestamp": "2026-03-02 15:30:22",
  "sender": "Alice",
  "message": "Hello Bob!",
  "encrypted": "5Xx9pLq2rM8vN3kH7jF6dG1sA4wE2rT9yU5iO8pB..."
}
👨‍💻 Author
Jamal Omar Haji Rabi
Cybersecurity Intern @ Syntecxhub
