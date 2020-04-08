#! /usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

dst_ip = "172.16.222.138"
src_port = RandShort()
dst_port=53
dst_timeout=10
#The client sends a UDP packet with the port number to connect to
udp_scan_resp = sr1(IP(dst=dst_ip)/UDP(dport=dst_port),timeout=dst_timeout)

#If the server sends no response to the client's UDP request packets for that port,it can be concluded that the port on the server is either open or filtered
if (str(type(udp_scan_resp))=="<type 'NoneType'>"):
    print "Open|Filtered"
#If the server responds to the client with a UDP packet, then that particular port is open on the server.
elif (udp_scan_resp.haslayer(UDP)):
    print "Open"
elif(udp_scan_resp.haslayer(ICMP)):
    #the server responds with an ICMP port unreachable error type 3 and code 3, meaning that the port is closed on the server.
    if(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code)==3):
        print "Closed|Filtered"
    
    #If the server responds to the client with an ICMP error type 3 and code 1, 2, 9, 10, or 13, then that port on the server is filtered.
    elif(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code) in [1,2,9,10,13]):
        print "Filtered"
elif(udp_scan_resp.haslayer(IP) and udp_scan_resp.getlayer(IP).proto==IP_PROTOS.udp):
    print "Open"