import argparse
import subprocess
import time
import random
import socket
import fcntl
import struct
import multiprocessing
import os
import signal
from datetime import datetime, timedelta

def get_ip_address(interface):
    # Get the IP address of the specified interface
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', interface[:15].encode())
        )[20:24])
        return ip_address
    except IOError:
        return None

def start_iperf_server_session(client_ip):
    port = int(client_ip.split('.')[2]) + 5200
    server_log_file = f'iperf3_server_{client_ip}.log'
    server_cmd = ['iperf3', '-s', '--logfile', server_log_file, '-p', str(port)]
    subprocess.Popen(server_cmd, stderr=subprocess.STDOUT, universal_newlines=True)

def start_iperf_server_sessions(other_clients):
    processes = []
    for client in other_clients:
        process = multiprocessing.Process(target=start_iperf_server_session, args=(client['ip'],))
        process.start()
        processes.append(process)
    return processes

def start_iperf_client_sessions(other_clients, local_ip):
    port = int(local_ip.split('.')[2]) + 5200
    # Start iperf3 client sessions
    processes = []
    for client in other_clients:
        if client ['ip'] != local_ip:
            bandwidth = random.randint(2, 10)
            client_log_file = f'iperf3_client_{client ["ip"]}.log'
            client_cmd = ['iperf3', '-c', client ['ip'], '-p', str(port), '-b', f'{bandwidth}M', '--logfile', client_log_file, '-t', '60',]
            subprocess.Popen(client_cmd, stderr=subprocess.STDOUT, universal_newlines=True)


def terminate_iperf_server_sessions(server_processes):
    for process in server_processes:
        process.terminate()
        process.join()


def main(num_clients):
    # Get the IP address of the eth0 interface
    eth0_ip = get_ip_address('eth0')

    # Generate a list of client IP addresses
    clients = [{'ip': f'172.16.1{i:02d}.51'} for i in range(1, num_clients + 1)]

    # Start iperf3 server sessions
    server_processes = start_iperf_server_sessions(clients)
    
    run_count = 0

    try:
        while True:
            # Start iperf3 client sessions
            start_iperf_client_sessions(clients, eth0_ip)

            # Sleep for 5 minutes before restarting the iperf3 server sessions
            time.sleep(62)
            
            if run_count == 10:
                # Terminate iperf3 server sessions
                terminate_iperf_server_sessions(server_processes)
    
                # Start new iperf3 server sessions
                server_processes = start_iperf_server_sessions(clients)
                run_count = 0
    except KeyboardInterrupt:
        # Clean up when interrupted
        terminate_iperf_server_sessions(server_processes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('num_clients', type=int, help='Number of iperf3 clients to start')
    args = parser.parse_args()

    main(args.num_clients)

