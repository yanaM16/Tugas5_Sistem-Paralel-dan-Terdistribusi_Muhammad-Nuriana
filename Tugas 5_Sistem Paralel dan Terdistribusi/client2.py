import socket
import threading
import sys

def receive_messages(client_socket):
    """Thread untuk menerima pesan dari server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  
            if message:
                print(f"Pesan dari server: {message}")  
        except:
            print("Koneksi ke server terputus.")
            client_socket.close()
            sys.exit()  

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('192.168.0.21', 12345)) 
        print("Terhubung ke server. Mulai chat...")
        
       
        thread = threading.Thread(target=receive_messages, args=(client,))
        thread.start()
        
        while True:
            message = input() 
            if message.lower() == 'quit': 
                print("Meninggalkan chat...")
                break
            if message:
                print(f"Anda: {message}") 
                client.send(message.encode('utf-8')) 
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Koneksi ditutup.")

if __name__ == "__main__":
    main()