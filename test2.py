import pyshark 
from threading import Thread
from time import sleep

capture = None 

def get_capture(page):
	global capture 
	try:
		capture = pyshark.LiveCapture(interface='eth0')
		filepath = "/root/Desktop/kali/fri_2/logs/"+page+".txt"
		print("hello2")
		capture.sniff(packet_count=10)
	
		def print_packet(pkt):
			try:
				filename = open(filepath, "a+")
				protocol =  pkt.transport_layer
				size = pkt.length
				time = pkt.sniff_time.strftime("%H:%M:%S.%f")
				dst_addr = pkt.ip.dst
				dst_port = pkt[pkt.transport_layer].dstport

				if protocol != None:
					data = "%s, %s, %s, %s, %s \n" % (protocol, time, size, dst_addr, dst_port)
					filename.write(data)
					filename.close()
			except AttributeError as e:
				#ignore packets that aren't TCP/UDP or IPv4
				pass

		capture.apply_on_packets(print_packet, timeout=20)

		print("hello")
		
	except Exception as e:
		print("Error with sniffer: ", e)
		pass


t = Thread(target=get_capture, args=("wikipage",)) 
t.start() 
sleep(1)
capture.close()



