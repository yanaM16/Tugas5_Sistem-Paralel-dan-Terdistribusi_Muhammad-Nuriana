import socket
import threading

clients = []
lock = threading.Lock() 

def broadcast(message, sender_socket):
    """Mengirim pesan ke semua client kecuali pengirim."""
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8')) 
                except:
                 
                    clients.remove(client)
                    client.close()

def handle_client(client_socket):
    """Menangani koneksi dari satu client."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  # Terima pesan
            if message: 
                print(f"Pesan diterima: {message}")
                broadcast(message, client_socket) 
        except:
           
            print("Koneksi client terputus.")
            with lock:
                if client_socket in clients:
                    clients.remove(client_socket)
            client_socket.close()
            break 

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.0.21', 12345 ))
    server.listen(5) 
    print("Server berjalan dan menunggu koneksi...")

    while True:
        try:
            client_socket, address = server.accept() 
            print(f"Koneksi baru dari {address}")
            with lock:
                clients.append(client_socket) 
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start() 
        except Exception as e:
            print(f"Error pada server: {e}")
            break 

if __name__ == "__main__":
    main()