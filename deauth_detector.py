from scapy.all import *
import os
import time

interface = "wlan1"  # Change this to your monitor mode interface

records = {} # Dictionary to count deauth packets from each source MAC address
attacker_mac = {} # Variable to store the MAC address of the detected attacker


def packet_handler(pkt):
    if pkt.haslayer(Dot11Deauth):
        source_mac = pkt.addr2
        target_mac = pkt.addr1

        global records
        global attacker_mac
        
        if (source_mac) in records : 

            records[source_mac].append(time.time())

            if len(records[source_mac]) == 5 :
               
                if records[source_mac][4] - records[source_mac][0] < 5 :  # Check if 5 deauth packets were sent within 5 seconds

                    if source_mac in attacker_mac and time.time() - attacker_mac[source_mac] < 60 :

                        pass # If the same attacker is already detected, ignore further alerts for the next 60 seconds
                    
                    else:
                        attacker_mac[source_mac] = time.time()

                        print(f"[*] Suspicious deauth activity detected from {source_mac}" f" targeting {target_mac}" f" at {time.ctime(pkt.time)}" f" frame speed:{getattr(pkt, "Rate", "N/A")}" f"reason code:{pkt[Dot11Deauth].reason}")

                        with open("attackerLog.txt", "a") as f:
                            f.write(f"[*] Suspicious deauth activity detected from {source_mac} targeting {target_mac} at {time.ctime(pkt.time)} frame speed:{getattr(pkt, "Rate", "N/A")} reason code:{pkt[Dot11Deauth].reason}\n")

                records[source_mac].pop(0) # Remove the oldest entry to keep the dictionary size manageable   
   
        else :
            records[source_mac] = [time.time()]
         
        
        print("It is not a deauth attack packet")

print(f"[*] {interface} dinleniyor. Deauth paketleri bekleniyor...")

try :
    sniff(iface=interface, prn=packet_handler, store=0)

except KeyboardInterrupt:
    print("Stopping deauthentication attack detector.")     