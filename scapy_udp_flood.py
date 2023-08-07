from scapy.all import *
import time
import threading

# Define the destination IP address and port number
ip = "172.16.14.1"
port = 9

# Set the TTL field of the IP header to 1
ttl = 1

# Define the size of the payload in bytes
payload_size = 56

# Calculate the number of packets per second to generate 100 Mbps of traffic
packets_per_second = 100000000 / (payload_size + 42)  # 42 bytes for the headers

# Set the number of packets to send per iteration
num_packets = int(packets_per_second / 10)  # Send 10 iterations per second

# Set the duration to run the script (in seconds)
duration = 360

# Define a function to send packets in a loop
def send_packets():
    # Get the start time for the thread
    start_time = time.time()

    # Create a loop to send the packets
    while True:
        # Create a list of packets to send
        packets = [IP(dst=ip, ttl=ttl)/UDP(dport=port)/Raw(b"X"*payload_size)] * num_packets

        # Send the packets using send()
        send(packets, verbose=False)

        # Check if the desired duration has been reached
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

while True:
    # Create a list to hold the threads
    threads = []

    # Create 5 threads to send packets
    for i in range(5):
        thread = threading.Thread(target=send_packets)
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for the threads to finish
    for thread in threads:
        thread.join()

    # Wait for 10 minutes before running the script again
    time.sleep(600)


