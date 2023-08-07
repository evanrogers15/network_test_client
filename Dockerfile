FROM gns3/ubuntu:focal as runtime

RUN apt-get update && apt-get install -y snmp iperf3 nuttcp
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update && apt-get install -y python3-pip
#RUN pip install --no-cache-dir --pre scapy[complete]
RUN pip install --no-cache-dir --pre scapy[basic]


# copy startup script
COPY scapy_udp_flood.py /home/scripts/scapy_udp_flood.py
COPY startup_nuttcp.sh /home/startup_nuttcp.sh
COPY startup_tailscale.sh /home/startup_tailscale.sh
COPY netflow_forwarder.py /home/scripts/netflow_forwarder.py
COPY client_traffic_generator.py /home/scripts/client_traffic_generator.py

#CMD ["/home/startup.sh"]
CMD ["bash"]
