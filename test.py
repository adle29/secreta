import pyshark 
from selenium import webdriver
from tor import get_browser
from time import sleep
import threading
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime as dt
from datetime import timedelta
from tbselenium.tbdriver import TorBrowserDriver

import sys

# condition = False
# caps = DesiredCapabilities.FIREFOX
# caps["marionette"] = True
# caps["binary"] = "/usr/bin/firefox"
# wait_time = 20
# stop_test = False

urls = {
	"wikipedia": "https://www.wikipedia.org/", 
	"wiki1": "https://en.wikipedia.org/wiki/World_War_II",
	"wiki2": "https://en.wikipedia.org/wiki/October_2016_Dyn_cyberattack",
	"wiki3": "https://en.wikipedia.org/wiki/Soviet_Union",
	"yahoo" : "https://www.yahoo.com/"
	}

with TorBrowserDriver("/usr/bin/tor-browser/") as browser:
	try:
		browser.get('https://check.torproject.org')
		browser.quit()
		stop_test = True 
	except Exception as e:
		print(e)
		pass

# class SThread(threading.Thread):
#     """Thread class with a stop() method. The thread itself has to check
#     regularly for the stopped() condition."""

#     def __init__(self, target, args=()):
#         super(SThread, self).__init__(target=target, args=args)
#         self._stop = threading.Event()

#     def stop(self):
#         self._stop.set()

#     def stopped(self):
#         return self._stop.isSet()

# def recollect_data(): 
# 	global stop_test
# 	# profile = webdriver.FirefoxProfile('/root/.mozilla/firefox/ukuk696t.default/')
# 	# profile.set_preference('network.proxy.type', 1)
# 	# profile.set_preference('network.proxy.socks', '127.0.0.1')
# 	# profile.set_preference('network.proxy.socks_port', 9150)
# 	# browser = webdriver.Firefox(profile)
# 	# browser.get('https://check.torproject.org/')

# 	for page in urls.keys(): 
# 		print("Request to %s" % page)
# 		#end = dt.now() + timedelta(seconds=wait_time)
# 		urlPath = urls[page]
# 		#make threads 
# 		sniffer_thread = SThread(target=get_capture, args=(page,))
# 		sniffer_thread.start()
# 		request_thread = SThread(target=web_request, args=(urlPath,))
# 		request_thread.start()
		
# 		#wait until t10 seconds 
# 		# now = dt.now()
# 		# while (end - now).total_seconds() > 0: 
# 		seconds = 0
# 		#progress = pb.ProgressBar(widgets=[Percentage(), Bar()], maxval = wait_time).start()
# 		while stop_test == False:#seconds <= wait_time:
# 			pass
# 			#progress.update(seconds)
# 			#sleep(1)
# 			#seconds += 1	
# 		stop_test = False
# 		#progress.update(wait_time)
# 		print()

# 		#stop threads 
# 		sniffer_thread.stop()
# 		#sniffer_thread.join()
# 		#request_thread.stop()
# 		#request_thread.join()

# 	#browser.close()

# def web_request(url):
# 	global stop_test
# 	with TorBrowserDriver("/usr/bin/tor-browser/") as browser:
# 		try:
# 			browser.get('https://check.torproject.org')
# 			browser.quit()
# 			stop_test = True 
# 		except Exception as e:
# 			print(e)
# 			pass


# def main():
# 	#recollect_data()
# 	#web_request("https://en.wikipedia.org/wiki/World_War_II")
# 	with TorBrowserDriver("/usr/bin/tor-browser/") as browser:
# 		try:
# 			browser.get('https://check.torproject.org')
# 			browser.quit()
# 			stop_test = True 
# 		except Exception as e:
# 			print(e)
# 			pass
# 	pass

# if __name__ == "__main__":
# 	main()
