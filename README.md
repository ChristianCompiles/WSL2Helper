# WSL2Helper

Scripts to forward UDP ports from Windows to WSL2

Commands to remember:
nc -ul 6699
nc -ul 7788

# WSL2

WSL2 allows developers to access a Linux environment inside of your standard Windows environment.
Drawbacks include potentially slower network traffic as this guide uses a port forwarding script to forward UDP traffic from the Windows environment to the WSL2 environment. A nice Youtube channel that deals with WSL2 and ROS: https://www.youtube.com/@polyhobbyist

# Installing WSL2 and Ubuntu 22.04

Open Powershell or Command Prompt in administator mode.

1. Install Ubuntu 22.04: `wsl --install --d Ubuntu-22.04`
2. Restart machine.

# Open WSL2 Coding Environment in VSCode

1. Open VSCode in Windows.
2. On left side panel, open Remote Explorer.
3. At top of Remote Explorer panel, select `WSL Targets.`
4. Select proper WSL2 environment.
5. Now you can open a folder in WSL2.

# UDP Windows Port Forwarding

1. Copy this code to your Windows environment and run it. This script allows the Windows computer to receive communications and then forward on to WSL2 because port forwarding command `netsh interface portproxy add` only forwards TCP ports. Running this script for the first time may cause a prompt to appear related to VSCode and firewall stuff; confirm/accept the prompt.
2. A simple way to check if the port is forwarding to WSL2 is to run `nc -lu <port_number>` in the WSL2 environment while traffic is being sent to the Windows environment.

```Python
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
    
    if not wsl2_ip:
        print(f"Issue finding WSL2 IP address.\nExiting")
        exit()

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
```
