import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

filename = "wikipedia.txt"
f = open("logs/"+filename)
list_X = []
list_Y = []
for line in f: 
	l = line.strip().split(',')
	y = int(l[2])
	x = datetime.strptime( l[1].strip(), '%H:%M:%S.%f')
	list_X.append(x)
	list_Y.append(y)

fig = plt.figure(figsize=(15,6))
plt.scatter(list_X, list_Y)


labels = [str(d)[:-6] for d in list_X]
plt.xlim(min(list_X), max(list_X))
plt.xlabel('Date')
plt.grid(True)
plt.ylabel('Size')
plt.title(filename)
plt.show()
fig.savefig('wikipedia.png')
plt.close()
