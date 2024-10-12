import socket
import threading

def forward(data, from_addr, to_addr):
    # Send the received data to the forwarding address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a new socket for sending
    sock.sendto(data, to_addr)
    print(f"Forwarded {len(data)} bytes from {from_addr} to {to_addr}")
    sock.close()  # Close the socket after sending

def listen_and_forward(listen_addr, forward_addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(listen_addr)
    
    print(f"UDP relay listening on {listen_addr}, forwarding to {forward_addr}")
    
    while True:
        data, addr = sock.recvfrom(1024)  # Receive data from the socket
        # Start a new thread for forwarding the received data
        threading.Thread(target=forward, args=(data, addr, forward_addr)).start()

if __name__ == "__main__":
    # Define the listening addresses for both ports
    listen_addr_1 = ("0.0.0.0", 6699)  # First port
    forward_addr_1 = ("172.23.184.17", 6699)  # WSL2 address for the first port
    
    listen_addr_2 = ("0.0.0.0", 7788)  # Second port
    forward_addr_2 = ("172.23.184.17", 7788)  # WSL2 address for the second port
    
    # Create threads to listen on both ports
    thread1 = threading.Thread(target=listen_and_forward, args=(listen_addr_1, forward_addr_1))
    thread2 = threading.Thread(target=listen_and_forward, args=(listen_addr_2, forward_addr_2))
    
    # Start both listening threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to finish (this should not happen in normal operation)
    thread1.join()
    thread2.join()
