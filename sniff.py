import pyshark 
from selenium import webdriver
from tor import get_browser
from time import sleep
from threading import Thread
from datetime import datetime as dt
from datetime import timedelta
from tbselenium.tbdriver import TorBrowserDriver

import sys
import os

condition = False
wait_time = 20
stop_test = False
capture = None
dirs = '/root/Desktop/kali/fri_2/logs/'

def web_request(browser, url):
	global stop_test
	try:
		browser.get(url)
		sleep(1)
		browser.close()
		sleep(1)
		stop_test = True 
	except Exception as e:
		print(e)
		pass

def get_capture(capture, folder, page):
	try:
		capture = pyshark.LiveCapture(interface='eth0')
		filepath = dirs+folder+'/'+page+".txt"
		
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
					#print(data)
					filename.write(data)
					filename.close()
			except AttributeError as e:
				#ignore packets that aren't TCP/UDP or IPv4
				pass

		capture.apply_on_packets(print_packet, timeout=20)
		
	except Exception as e:
		print("Error with sniffer: ", e)
		pass

def recollect_data(urlPath, folder, page): 
	global stop_test
	global capture

	print("Request to %s" % page)
	browser = TorBrowserDriver("/usr/bin/tor-browser/")
	directory = dirs+folder

	if not os.path.exists(directory):
		os.makedirs(directory)

	sniffer_thread = Thread(target=get_capture, args=(capture, folder, page,))
	sniffer_thread.start()
	request_thread = Thread(target=web_request, args=(browser, urlPath,))
	request_thread.start()
	
	while stop_test == False:
		pass

	stop_test = False

def main():
	# "https://en.wikipedia.org/wiki/October_2016_Dyn_cyberattack" --- wikipage1
	# "https://en.wikipedia.org/wiki/Soviet_Union" --- wikipage2
	# "https://en.wikipedia.org/wiki/World_War_II" --- wikipage3 
	# "https://www.yahoo.com/" --- yahoo 
	# "http://inverarteartgallery.com/" --- inverarte
	# "https://www.amazon.com/" --- amazon
	# "http://www.utexas.edu/" --- utexas
	# "http://www.ign.com/" ---- ign
	# "http://www.sparknotes.com/lit/twocities/section2.rhtml" ---sparknotes
	# "https://defcon.ru/" --- defcon
	# "http://www.cnn.com/" --- cnn
 
	for i in range(1,41):
		url = "http://www.cnn.com/"
		folder = 'cnn'
		name = folder+'_'+str(i)
		recollect_data(url, folder, name)

if __name__ == "__main__":
	main()
