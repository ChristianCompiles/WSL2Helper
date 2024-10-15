import socket
import threading
import subprocess

def get_wsl_ip():
    try:
        # Run the command 'wsl hostname -I' and capture the output
        result = subprocess.run(['wsl', 'hostname', '-I'], capture_output=True, text=True, check=True)
        
        # The output is stored in result.stdout
        ip_address = result.stdout.strip()  # Remove any leading/trailing whitespace
        return ip_address
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while getting the WSL IP address: {e}")
        return None
    
def forward(data, from_addr, to_addr):
    # Send the received data to the forwarding address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a new UDP socket for sending
    sock.sendto(data, to_addr)
    #print(f"Forwarded {len(data)} bytes from {from_addr} to {to_addr}")
    sock.close()  # Close the socket after sending

def listen_and_forward(listen_addr, forward_addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(listen_addr)
    
    print(f"UDP relay listening on {listen_addr}, forwarding to {forward_addr}")
    
    while True:
        data, addr = sock.recvfrom(4096)  # Receive data from the socket
        # Start a new thread for forwarding the received data
        threading.Thread(target=forward, args=(data, addr, forward_addr)).start()
        #time.sleep(0.1) # Not sure if we can sleep any significant amount of time 

if __name__ == "__main__":
    ports = [6699, 7788]  # Ports to listen on Windows and send to WSL2.
    wsl2_ip = get_wsl_ip()
    
    if wsl2_ip:
        print(f"WSL IP Address: {wsl2_ip}")

        # Create a list to hold the threads
        threads = []
        
        for port in ports:
            listen_addr = ("0.0.0.0", port)
            forward_addr = (wsl2_ip, port)
            thread = threading.Thread(target=listen_and_forward, args=(listen_addr, forward_addr))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
    else:
        print(f"Issue finding WSL2 IP address.\nExiting")
