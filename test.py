import pyshark 
from datetime import datetime as dt
from datetime import timedelta

from tbselenium.tbdriver import TorBrowserDriver

with TorBrowserDriver("/usr/bin/tor-browser/") as driver:
    driver.get('https://check.torproject.org')


# wait_time = 10

# def get_capture(page):
# 	filepath = "logs/"+page+".txt"
# 	capture = pyshark.LiveCapture(interface='eth0')
# 	capture.sniff(packet_count=10)
# 	end = dt.now() + timedelta(seconds=wait_time)

# 	def print_packet(pkt):
# 		# now = dt.now()
# 		# if (end - now).total_seconds() <= 0:
# 		# 	capture.close()

# 		try:
# 			#print("here")
# 			filename = open(filepath, "a+")

# 			protocol =  pkt.transport_layer
			
# 			size = pkt.length
# 			time = pkt.sniff_time.strftime("%H:%M:%S.%f")
# 			# delta = pkt.delta
# 			# no = pkt.no
# 			dst_addr = pkt.ip.dst
# 			dst_port = pkt[pkt.transport_layer].dstport

# 			data = "%s, %s, %s, %s, %s \n" % (protocol, time, size, dst_addr, dst_port)
# 			print(data)

# 			if protocol != None:
# 				data = "%s, %s, %s, %s, %s \n" % (protocol, time, size, dst_addr, dst_port)
# 				print(data)
# 				filename.write(data)
# 				filename.close()
# 		except Exception as e:
# 			#ignore packets that aren't TCP/UDP or IPv4
# 			print(e)
# 			pass

# 	capture.apply_on_packets(print_packet, timeout=100)
# 	capture.close()


# get_capture("output1")