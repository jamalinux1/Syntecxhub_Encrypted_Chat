import socket
import threading
import sys
from encryption import AESCipher

class ChatClient:
    def __init__(self):
        self.client_socket = None
        self.running = False
        self.cipher = None
        
    def connect(self, host='127.0.0.1', port=5555, key="MySecretKey123!@#"):
        """Connect to the chat server"""
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            
            # Initialize encryption with pre-shared key
            self.cipher = AESCipher(key)
            
            # Get and send name
            name = input("Enter your name: ").strip()
            if not name:
                name = "Anonymous"
            self.client_socket.send(name.encode())
            
            # Receive welcome message
            welcome_encrypted = self.client_socket.recv(1024).decode()
            welcome = self.cipher.decrypt(welcome_encrypted)
            print(f"\n{welcome}\n")
            
            self.running = True
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Start sending messages
            self.send_messages()
            
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.disconnect()
    
    def receive_messages(self):
        """Receive and display messages"""
        while self.running:
            try:
                # Receive encrypted message
                encrypted_msg = self.client_socket.recv(1024).decode()
                if not encrypted_msg:
                    break
                
                # Decrypt and display
                message = self.cipher.decrypt(encrypted_msg)
                print(f"\r{message}\nYou: ", end="")
                
            except Exception as e:
                if self.running:
                    print(f"\nReceive error: {e}")
                break
    
    def send_messages(self):
        """Send messages to server"""
        print("Type your messages (type 'quit' to exit):")
        
        while self.running:
            try:
                message = input("You: ")
                
                if message.lower() == 'quit':
                    break
                
                if message.strip():
                    # Encrypt and send
                    encrypted = self.cipher.encrypt(message)
                    self.client_socket.send(encrypted.encode())
                    
            except Exception as e:
                print(f"Send error: {e}")
                break
        
        self.disconnect()
    
    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        print("\nDisconnected from chat")

if __name__ == "__main__":
    print("=" * 50)
    print("ENCRYPTED CHAT CLIENT")
    print("=" * 50)
    
    # Get server details
    host = input("Enter server IP (press Enter for 127.0.0.1): ").strip()
    if not host:
        host = '127.0.0.1'
    
    port = input("Enter port (press Enter for 5555): ").strip()
    if not port:
        port = 5555
    else:
        port = int(port)
    
    key = input("Enter pre-shared key (press Enter for default): ").strip()
    if not key:
        key = "MySecretKey123!@#"
    
    # Connect to server
    client = ChatClient()
    
    try:
        client.connect(host, port, key)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        client.disconnect()