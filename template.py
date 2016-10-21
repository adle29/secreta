#load pyshark module 
import pyshark 

#declare live capture module
capture = pyshark.LiveCapture(interface='eth0')

#start sniffing an interface
capture.sniff(packet_count=10)

#print packet information 
def print_packet(pkt): 
	# ['delta', 'destination', 'info', 'ip id', 'length', 'no', 
	# 'protocol', 'source', 'stream', 'summary_line', 'time', 'window']
	#print packet information 
	print(pkt.protocol)

#add print function to check each packet
capture.apply_on_packets(print_packet, timeout=100)
