import pyshark 
from selenium import webdriver
from tor import get_browser
from time import sleep
import threading
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime as dt
from datetime import timedelta
import sys
import progressbar as pb
from progressbar import Percentage, Bar

condition = False
caps = DesiredCapabilities.FIREFOX
caps["marionette"] = True
caps["binary"] = "/usr/bin/firefox"
wait_time = 20
stop_test = False

urls = {
	"wikipedia": "https://www.wikipedia.org/", 
	"yahoo" : "https://www.yahoo.com/"
	}

class SThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, target, args=()):
        super(SThread, self).__init__(target=target, args=args)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

def recollect_data(): 
	global stop_test
	# profile = webdriver.FirefoxProfile('/root/.mozilla/firefox/ukuk696t.default/')
	# profile.set_preference('network.proxy.type', 1)
	# profile.set_preference('network.proxy.socks', '127.0.0.1')
	# profile.set_preference('network.proxy.socks_port', 9150)
	# browser = webdriver.Firefox(profile)
	# browser.get('https://check.torproject.org/')

	for page in urls.keys(): 
		print("Request to %s" % page)
		#end = dt.now() + timedelta(seconds=wait_time)
		urlPath = urls[page]
		#make threads 
		sniffer_thread = SThread(target=get_capture, args=(page,))
		sniffer_thread.start()
		request_thread = SThread(target=web_request, args=(urlPath,))
		request_thread.start()
		
		#wait until t10 seconds 
		# now = dt.now()
		# while (end - now).total_seconds() > 0: 
		seconds = 0
		#progress = pb.ProgressBar(widgets=[Percentage(), Bar()], maxval = wait_time).start()
		while stop_test == False:#seconds <= wait_time:
			pass
			#progress.update(seconds)
			#sleep(1)
			#seconds += 1	
		stop_test = False
		#progress.update(wait_time)
		print()

		#stop threads 
		sniffer_thread.stop()
		#sniffer_thread.join()
		#request_thread.stop()
		#request_thread.join()

	#browser.close()

def web_request(url):
	global stop_test
	profile = webdriver.FirefoxProfile('/root/.mozilla/firefox/ukuk696t.default/')
	profile.set_preference('network.proxy.type', 1)
	profile.set_preference('network.proxy.socks', '127.0.0.1')
	profile.set_preference('network.proxy.socks_port', 9150)
	browser = webdriver.Firefox(profile)
	#browser.get('https://check.torproject.org/')

	try:
		browser.get(url)
		browser.quit()
		stop_test = True 
	except Exception as e:
		print(e)
		pass

def get_capture(page):
	try:
		filepath = "logs/"+page+".txt"
		capture = pyshark.LiveCapture(interface='eth0')
		capture.sniff(packet_count=10)
		end = dt.now() + timedelta(seconds=wait_time)
	
		def print_packet(pkt):
			#print data
			#print("sniffing "+ str(page))
			# now = dt.now()
			# if (end - now).total_seconds() <= 0:
			# 	capture.close()

			try:
				filename = open(filepath, "a+")
				protocol =  pkt.transport_layer
				size = pkt.length
				time = pkt.sniff_time.strftime("%H:%M:%S.%f")
				# delta = pkt.delta
				# no = pkt.no
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
		
	except:
		pass


def main():
	recollect_data()

if __name__ == "__main__":
	main()



#get_capture()

# for packet in capture.sniff_continuously(packet_count=5):
#     print ('Just arrived:', packet)


# >>> capture = pyshark.RemoteCapture('192.168.69.169', 'eth0')
# >>> capture.sniff(timeout=50)
# >>> capture
# https://github.com/KimiNewt/pyshark

# capture = pyshark.RemoteCapture('192.168.69.169', 'eth0')
# capture.sniff(timeout=50)

# for packet in capture.sniff_continuously(packet_count=5):
#     print ('Just arrived:', packet)

# for pack in capture:
# 	print(pack.transport_layer)

# def print_dns_info(pkt):
#     if pkt.dns.qry_name:
#         print ('DNS Request from %s: %s' % (pkt.ip.src, pkt.dns.qry_name))
#     elif pkt.dns.resp_name:
#         print ('DNS Response from %s: %s' % (pkt.ip.src, pkt.dns.resp_name))
 
# ['delta', 'destination', 'info', 'ip id', 'length', 'no', 
# 'protocol', 'source', 'stream', 'summary_line', 'time', 'window']