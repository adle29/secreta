import pyshark 
from selenium import webdriver
from time import sleep
from threading import Thread
from datetime import datetime as dt
from datetime import timedelta
from tbselenium.tbdriver import TorBrowserDriver

import sys
import os
import glob
import shutil

"""
	CONSTANTS 
"""
START = 37
SAMPLE_SIZE = 40
DIR = os.getcwd()+'/data/'

"""
	CONDITION VARIABLES  
"""
stop_test = False
alive = True
sniffer_running = False


"""
	Loads a url from the tor browswer
	url: string containing the address of the website
	browser: tor browser device based on selenium 
"""
def web_request(browser, url):
	global stop_test
	global alive
	try:
		browser.get(url)
		sleep(0.5)
		browser.close()
		sleep(0.5)
		stop_test = True 
		print("[+]Sending signal to stop sniffer.")
	except Exception as e:
		print(e)
		pass

	alive = False


"""
	Starts the sniffer on the ethernet port 
	folder: directory to store files with sniff data
	page: file name for the sniff data 
"""
def get_capture(folder, page):
	global sniffer_running
	# try:
	
	capture = pyshark.LiveCapture(interface='eth0')
	filepath = DIR+folder+'/'+page+".txt"

	for pkt in capture.sniff_continuously():
		if(not alive):
			print("[+]Stopped sniffer")
			sniffer_running = False
			return 
		try: 
			filename = open(filepath, "a+")
			protocol =  pkt.transport_layer
			size = pkt.length
			time = pkt.sniff_time.strftime("%H:%M:%S.%f")
			dst_addr = pkt.ip.dst
			dst_port = pkt[pkt.transport_layer].dstport

			if protocol != None:
				data = "%s, %s, %s, %s, %s, %s \n" % (folder, protocol, time, size, dst_addr, dst_port)
				filename.write(data)
				filename.close()
		except AttributeError as e:
			#ignore packets that aren't TCP/UDP or IPv4
			pass

"""
	Multi-threaded function that runs two threads: the sniffer and the selenium tor browser
	requesting a url website. 
	urPath: url of the website
	folder: directory to store files with sniff data
	page: file name for the sniff data 

	**details: 3 conditions variables wait until the website is loaded, the thread is alive, 
	and the sniffer stops running  
"""
def collect_data(urlPath, folder, page): 
	global stop_test
	global alive
	global sniffer_running

	print("[+]Request to %s" % page)
	try: 
		browser = TorBrowserDriver("/usr/bin/tor-browser/")
		directory = DIR+folder

		if not os.path.exists(directory):
			os.makedirs(directory)

		sniffer_running = True

		sniffer_thread = Thread(target=get_capture, args=(folder, page,))
		sniffer_thread.start()
		request_thread = Thread(target=web_request, args=(browser, urlPath,))
		request_thread.start()

		while(alive or sniffer_running):
			pass
		
		while(not stop_test):
			pass

		stop_test = False
		alive = True
	except KeyboardInterrupt:
		print("[-] Interrupted")
		sys.exit(0)
	except:
		collect_data(urlPath, folder, page)
		pass

"""
	Clean files in directory tmp from the capture, pyshark creates a bunch of
	temporary files that my flood the memory
"""
def clean_tmp_folder():
	files = glob.glob('/tmp/*')
	for f in files:
		if os.path.isdir(f):
			#os.removedirs(f)
			shutil.rmtree(f, ignore_errors=False, onerror=None)
		else:
			os.remove(f)

"""
	Start collecting samples from file loaded 
	SAMPLE_SIZE: how many samples to take from each website 
"""
def collect_samples(websites):
	fd = open(websites)
	for line in fd: 
		b = line.split(',')
		url = b[1].strip()
		folder = b[0].strip()
		try:
			clean_tmp_folder()
		except:
			pass
		for i in range(START, SAMPLE_SIZE+1):
			name = folder + '_' + str(i)
			collect_data(url, folder, name)

def main():
	collect_samples('websites.txt')

if __name__ == "__main__":
	main()
