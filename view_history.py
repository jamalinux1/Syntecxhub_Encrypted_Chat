import os
import json
from encryption import AESCipher
from datetime import datetime

def view_chat_history(log_file=None, key="MySecretKey123!@#"):
    """View and analyze chat history"""
    
    cipher = AESCipher(key)
    
    print("=" * 70)
    print("🔐 ENCRYPTED CHAT HISTORY VIEWER".center(70))
    print("=" * 70)
    
    # If no log file specified, find the most recent one
    if not log_file:
        log_files = [f for f in os.listdir('.') if f.startswith('chat_log_') and f.endswith('.txt')]
        if not log_files:
            print("❌ No chat log files found in current directory!")
            return
        
        # Sort by date (newest first)
        log_files.sort(reverse=True)
        print("\n📋 Available log files:")
        for i, f in enumerate(log_files[:5], 1):  # Show last 5
            file_time = f.replace('chat_log_', '').replace('.txt', '')
            try:
                # Try to format the timestamp
                dt = datetime.strptime(file_time, '%Y%m%d_%H%M%S')
                print(f"   {i}. {f} ({dt.strftime('%Y-%m-%d %H:%M:%S')})")
            except:
                print(f"   {i}. {f}")
        
        choice = input("\nSelect file number (or press Enter for most recent): ").strip()
        if choice and choice.isdigit() and 1 <= int(choice) <= len(log_files[:5]):
            log_file = log_files[int(choice)-1]
        else:
            log_file = log_files[0]
            print(f"📄 Using most recent: {log_file}")
    
    print(f"\n📄 Analyzing: {log_file}")
    print("-" * 70)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"\n📊 Total messages: {len(lines)}")
        print("\n" + "=" * 70)
        print("📜 CHAT HISTORY (with encryption status)".center(70))
        print("=" * 70)
        
        # Process each line
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # Parse the log line
            # Format: [timestamp] sender: message
            if '] ' in line:
                timestamp_part = line.split('] ')[0] + ']'
                rest = line.split('] ')[1]
                
                if ': ' in rest:
                    sender, message = rest.split(': ', 1)
                    
                    print(f"\n📝 Message #{i}")
                    print(f"   🕐 {timestamp_part}")
                    print(f"   👤 {sender}")
                    
                    # Show encrypted version
                    if sender != "SYSTEM":
                        encrypted = cipher.encrypt(message)
                        print(f"   🔒 Encrypted: {encrypted[:50]}...")
                        print(f"   🔓 Decrypted: {message}")
                    else:
                        print(f"   ℹ️ System: {message}")
                    
                    print("-" * 50)
        
        # Save to a separate encrypted history file
        save_choice = input("\n💾 Save encrypted version to separate file? (y/n): ").strip().lower()
        if save_choice == 'y':
            encrypted_file = log_file.replace('.txt', '_encrypted.txt')
            with open(encrypted_file, 'w', encoding='utf-8') as f:
                f.write("ENCRYPTED CHAT HISTORY\n")
                f.write("=" * 50 + "\n\n")
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if '] ' in line:
                        timestamp_part = line.split('] ')[0] + ']'
                        rest = line.split('] ')[1]
                        
                        if ': ' in rest:
                            sender, message = rest.split(': ', 1)
                            
                            if sender != "SYSTEM":
                                encrypted = cipher.encrypt(message)
                                f.write(f"{timestamp_part} {sender}: {encrypted}\n")
                            else:
                                f.write(f"{timestamp_part} {sender}: {message}\n")
            
            print(f"✅ Encrypted history saved to: {encrypted_file}")
            
    except Exception as e:
        print(f"❌ Error reading log file: {e}")

def create_encrypted_history_report(log_file=None, key="MySecretKey123!@#"):
    """Create a detailed report with both encrypted and decrypted messages"""
    
    cipher = AESCipher(key)
    
    if not log_file:
        log_files = [f for f in os.listdir('.') if f.startswith('chat_log_') and f.endswith('.txt')]
        if not log_files:
            print("❌ No chat log files found!")
            return
        log_files.sort(reverse=True)
        log_file = log_files[0]
    
    report_file = log_file.replace('.txt', '_report.json')
    report_data = {
        'log_file': log_file,
        'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'messages': []
    }
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if '] ' in line:
                timestamp_part = line.split('] ')[0] + ']'
                rest = line.split('] ')[1]
                
                if ': ' in rest:
                    sender, message = rest.split(': ', 1)
                    
                    msg_entry = {
                        'timestamp': timestamp_part.strip('[]'),
                        'sender': sender,
                        'message': message
                    }
                    
                    if sender != "SYSTEM":
                        msg_entry['encrypted'] = cipher.encrypt(message)
                    
                    report_data['messages'].append(msg_entry)
        
        # Save report
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Detailed report saved to: {report_file}")
        return report_file
        
    except Exception as e:
        print(f"❌ Error creating report: {e}")
        return None

if __name__ == "__main__":
    while True:
        print("\n" + "=" * 70)
        print("🔐 ENCRYPTED CHAT HISTORY TOOL".center(70))
        print("=" * 70)
        print("1. View chat history (with encryption)")
        print("2. Generate JSON report (with encrypted messages)")
        print("3. Exit")
        print("-" * 70)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            view_chat_history()
        elif choice == '2':
            create_encrypted_history_report()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")