import socket
import threading
import datetime
from encryption import AESCipher, KeyExchange

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5555, key="MySecretKey123!@#"):
        self.host = host
        self.port = port
        self.key = key
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Store connected clients
        self.clients = []
        self.client_names = []
        self.client_addresses = []
        
        # Initialize encryption
        self.cipher = AESCipher(key)
        
        # Message logging
        self.log_file = f"chat_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
    def start(self):
        """Start the server"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print("\n" + "="*60)
            print("🔐 ENCRYPTED CHAT SERVER STARTED")
            print("="*60)
            print(f"📡 Host: {self.host}")
            print(f"🔌 Port: {self.port}")
            print(f"🔑 Pre-shared key: {self.key}")
            print(f"📝 Log file: {self.log_file}")
            print("="*60)
            print("Waiting for clients... (Ctrl+C to stop)\n")
            
            # Log server start
            self.log_message("SYSTEM", "Server started")
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"📞 New connection from {address[0]}:{address[1]}")
                
                # Handle client in a new thread
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                thread.daemon = True
                thread.start()
                
        except KeyboardInterrupt:
            print("\n\n👋 Server shutting down...")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.server_socket.close()
            self.log_message("SYSTEM", "Server stopped")
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        try:
            # Get client name
            client_socket.send("Enter your name: ".encode())
            name = client_socket.recv(1024).decode().strip()
            
            if not name:
                name = f"User_{len(self.clients)}"
            
            # Add client to lists
            self.clients.append(client_socket)
            self.client_names.append(name)
            self.client_addresses.append(address)
            
            # Send welcome message
            welcome = f"✨ Welcome {name}! You're connected to encrypted chat. Type 'quit' to exit."
            encrypted_welcome = self.cipher.encrypt(welcome)
            client_socket.send(encrypted_welcome.encode())
            
            # Broadcast join message
            join_msg = f"🔵 {name} joined the chat!"
            self.broadcast(join_msg, client_socket)
            self.log_message("SYSTEM", f"{name} joined from {address[0]}")
            
            print(f"✅ {name} connected from {address[0]}:{address[1]}")
            print(f"👥 Active users: {len(self.clients)}")
            
            # Handle messages from this client
            while True:
                try:
                    # Receive encrypted message
                    encrypted_data = client_socket.recv(1024).decode()
                    if not encrypted_data:
                        break
                    
                    # Decrypt message
                    message = self.cipher.decrypt(encrypted_data)
                    
                    if message.lower() == 'quit':
                        break
                    
                    # Format timestamp
                    timestamp = datetime.datetime.now().strftime('%H:%M')
                    
                    # Format and broadcast
                    formatted_msg = f"[{timestamp}] {name}: {message}"
                    print(f"📨 {formatted_msg}")
                    
                    # Log the message
                    self.log_message(name, message)
                    
                    # Broadcast to all other clients
                    self.broadcast(formatted_msg, client_socket)
                    
                except Exception as e:
                    print(f"Error receiving from {name}: {e}")
                    break
                    
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            # Remove client on disconnect
            self.remove_client(client_socket)
    
    def remove_client(self, client_socket):
        """Remove a client from the lists"""
        if client_socket in self.clients:
            index = self.clients.index(client_socket)
            name = self.client_names[index]
            address = self.client_addresses[index]
            
            self.clients.remove(client_socket)
            self.client_names.pop(index)
            self.client_addresses.pop(index)
            client_socket.close()
            
            # Broadcast leave message
            leave_msg = f"🔴 {name} left the chat!"
            self.broadcast(leave_msg, None)
            self.log_message("SYSTEM", f"{name} left")
            
            print(f"❌ {name} disconnected")
            print(f"👥 Active users: {len(self.clients)}")
    
    def broadcast(self, message, sender_socket):
        """Broadcast message to all clients except sender"""
        try:
            encrypted_msg = self.cipher.encrypt(message)
            
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.send(encrypted_msg.encode())
                    except:
                        pass
        except Exception as e:
            print(f"Broadcast error: {e}")
    
    def log_message(self, sender, message):
        """Log messages to file"""
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {sender}: {message}\n")
        except Exception as e:
            print(f"Logging error: {e}")

def main():
    print("=" * 60)
    print("🔐 ENCRYPTED CHAT SERVER - SETUP")
    print("=" * 60)
    
    # Get server settings
    host = input("Enter server IP [127.0.0.1]: ").strip()
    if not host:
        host = '127.0.0.1'
    
    try:
        port = input("Enter port [5555]: ").strip()
        if not port:
            port = 5555
        else:
            port = int(port)
    except:
        port = 5555
        print("Using default port 5555")
    
    key = input("Enter pre-shared key [MySecretKey123!@#]: ").strip()
    if not key:
        key = "MySecretKey123!@#"
    
    # Optional key exchange demo
    demo = input("\nShow key exchange demonstration? (y/n): ").strip().lower()
    if demo == 'y':
        KeyExchange.simulate_key_exchange()
    
    input("\nPress Enter to start server...")
    
    # Start server
    server = ChatServer(host, port, key)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")

if __name__ == "__main__":
    main()