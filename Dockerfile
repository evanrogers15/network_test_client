FROM gns3/ubuntu:focal

RUN apt-get update && apt-get install -y snmp iperf3 nuttcp
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --no-cache-dir --pre scapy[basic]

COPY startup_nuttcp.sh /home/scripts/startup/nuttcp.sh
COPY startup_tailscale.sh /home/scripts/startup/tailscale.sh
COPY netflow_forwarder.py /home/scripts/netflow_forwarder.py
COPY client_traffic_generator.py /home/scripts/traffic/client_traffic_generator.py
COPY scapy_udp_flood.py /home/scripts/traffic/scapy_udp_flood.py

#CMD ["/home/startup.sh"]
CMD ["bash"]
