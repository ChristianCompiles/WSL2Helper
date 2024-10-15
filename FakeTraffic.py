import socket
import subprocess
import threading
import time

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

def send_udp_traffic(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"This message for {ip}:{port}"
    while True: 
        sock.sendto(message.encode(), (ip, port))
        print(f"Sent: {message} to {ip}:{port}")
        time.sleep(1)
    #sock.close()

def start_sending(ip, port):
    send_udp_traffic(ip, port)

if __name__ == "__main__":
    ports = [6699, 7788]  # List of ports to send traffic to
    wsl2_ip = get_wsl_ip()
    
    if wsl2_ip:
        print(f"WSL IP Address: {wsl2_ip}")

        # Create a list to hold the threads
        threads = []

        # Start a thread for each port
        for port in ports:
            thread = threading.Thread(target=start_sending, args=(wsl2_ip, port))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print("Finished sending traffic.")
