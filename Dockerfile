FROM gns3/ubuntu:focal as runtime

RUN apt-get update && apt-get install -y snmp iperf3 nuttcp
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# now make a builder image to create trafgen
FROM runtime as builder

RUN apt-get update && apt-get install -y git make gcc g++ flex bison pkg-config\
  libncurses-dev libcli-dev libgeoip-dev libnetfilter-conntrack-dev\
  libnl-3-dev libnl-route-3-dev libnl-genl-3-dev libpcap-dev libsodium-dev\
  libnet1-dev

RUN git clone https://github.com/netsniff-ng/netsniff-ng.git
RUN cd netsniff-ng \
  && ./configure \
  && make trafgen \
  && make trafgen_install || :
#that last trick is to suppress the error caused my the makefile.  Doesn't matter


#the final image, needs bash for scripts
FROM runtime

ENV SOURCE_IP 192.168.1.10
ENV TARGET_IP 192.168.1.255
ENV TARGET_MAC ff:ff:ff:ff:ff:ff
ENV SOURCE_MAC 11:22:33:44:55:66
ENV TARGET_UDP_PORT 9
ENV SOURCE_UDP_PORT 9
ENV PACKETS 0
ENV RATE 0

RUN apt-get update && apt-get install -y python3-pip
#RUN pip install --no-cache-dir --pre scapy[complete]
RUN pip install --no-cache-dir --pre scapy[basic]


COPY --from=builder /netsniff-ng/trafgen/trafgen /usr/local/sbin/trafgen

# copy startup script
COPY gencfg /home/gencfg
COPY generate.sh /home/generate.sh
COPY scapy_udp_flood.py /home/scripts/scapy_udp_flood.py
COPY iperf3_server.py /home/scripts/iperf3_server.py
COPY startup_nuttcp.sh /home/startup_nuttcp.sh
COPY startup_tailscale.sh /home/startup_tailscale.sh
COPY iperf3_client_server.py /home/scripts/iperf3_client_server.py
COPY netflow_forwarder.py /home/scripts/netflow_forwarder.py

#CMD ["/home/startup.sh"]
CMD ["bash"]
