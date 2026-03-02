from encryption import KeyExchange
import time

print("=" * 50)
print("KEY EXCHANGE DEMONSTRATION")
print("=" * 50)

# Simulating key exchange between client and server
print("\n1. Server generates a secure key:")
server_key = KeyExchange.generate_key()
print(f"   Server key: {server_key}")
print(f"   Key hash: {KeyExchange.hash_key(server_key)}")

print("\n2. Key is shared with client (in real world, this would be secure):")
time.sleep(1)
print("   🔐 Sending key through secure channel...")
client_key = server_key  # In real world, this would be transmitted securely

print("\n3. Client receives and stores the key:")
print(f"   Client received key: {client_key}")
print(f"   Key hash verification: {KeyExchange.hash_key(client_key)}")

print("\n4. Both sides now have the same key for AES encryption!")
print("   All messages will be encrypted with this key.")

print("\n⚠️ SECURITY NOTES:")
print("   - In production, use asymmetric encryption for key exchange")
print("   - Keys should never be transmitted in plain text")
print("   - Consider using Diffie-Hellman key exchange")
print("   - Rotate keys periodically for better security")