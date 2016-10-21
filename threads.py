import time
import threading 
import datetime as DT

def worker(cond):
	i = 0 
	while True:
		with cond: 
			cond.wait()
			print(str(i))
			i += 1
			time.sleep(0.01)

cond = threading.Condition()
t = threading.Thread(target=worker, args=(cond,))
t.daemon = True 
t.start() 
start = DT.datetime.now()

while True:
	now = DT.datetime.now()
	if (now-start).total_seconds() > 60: break
	if now.second % 2:
		with cond:
			cond.notify()