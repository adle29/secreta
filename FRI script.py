from __future__ import print_function
from __future__ import division
from collections import Counter
from glob import glob
import numpy as np

from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
from sklearn import svm
import matplotlib.pyplot as plt
from random import randint

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# Variables
trials = 1000
classifier = svm.SVC(kernel = 'linear')
# classifier = GaussianNB()
# classifier = KNeighborsClassifier(1)

# Helper functions
def parse_timestamp(timestamp):
  hours, minutes, seconds = timestamp.split(":")
  time = int(hours) * 60 * 60 * (10**6) + int(minutes) * 60 * (10**6) + int(float(seconds) * (10**6))
  return time

def process_file(filename):
  f = open(filename)
  lines = f.readlines()

  time_deltas = []
  sizes = []
  unique_connections = set()
  
  for i in range(0, len(lines)):
    line = lines[i]
    protocol, timestamp, size, destination, port = line.split(", ")

    unique_connections.add((destination, port))

    sizes.append(size)

    if i == 0:
      last_time = parse_timestamp(timestamp)
      
    current_time = parse_timestamp(timestamp)
    time_deltas.append(current_time - last_time)
    last_time = current_time

  time_delta_histogram = dict(Counter(time_deltas))
  size_histogram = dict(Counter(sizes))
      
  return [len(unique_connections), time_delta_histogram, size_histogram]


""" 1. READ IN RAW DATA FOR EACH FILE """
# all_file_data[i] holds the pre-processed data of the i'th file
all_file_data = []

# set of all time_deltas/sizes encountered in any of the files
all_unique_time_deltas  = set()
all_unique_sizes = set()

# a map that assigns URLs to IDs. Just to work with numbers
url_to_nums = {}

# all_file_url_num[i] holds the ID for the URL that the i'th file corresopnds to.
# ex. if the 5th file is Amazon and Amazon has ID 7, then all_file_url_num[4] = 7
all_file_url_num = []

for filename in glob('data/*'):
    # assumes the files are in data/ and in the format <website>_<id>.txt
    file = filename.replace(".txt", "")
    url = file.split("_", 1)[0]

    # find the URL's ID. (make one if necessary)
    if url in url_to_nums:
      num = url_to_nums[url]
    else:
      num = len(url_to_nums)
      url_to_nums[url] = num
      print(num, url)

    all_file_url_num.append(num)

    # process the file
    file_data = process_file(filename)
    num_unique_connections, time_delta_histogram, size_histogram = file_data

    all_file_data.append(file_data)
    all_unique_time_deltas.update(time_delta_histogram.keys())
    all_unique_sizes.update(size_histogram.keys())

all_unique_time_deltas = np.array(list(all_unique_time_deltas))
all_unique_sizes = np.array(list(all_unique_sizes))

print(1)

""" 2. BUILD PARAMETERS FOR EACH FILE """

# all_file_params[i] holds the ML parameters of the i'th file
all_file_params = []

for file_data in all_file_data:
  num_unique_connections, time_delta_histogram, size_histogram = file_data
  
  file_params = []

  # add # connections to the params
  file_params.append(num_unique_connections)

  # add time_delta histogram to params
  for time_delta in all_unique_time_deltas:
    file_params.append(time_delta_histogram[time_delta] if time_delta in time_delta_histogram else 0)

  # add size histogram to params
  for size in all_unique_sizes:
    file_params.append(size_histogram[size] if size in size_histogram else 0)
    
  all_file_params.append(file_params)

all_file_params = np.array(all_file_params)

print(2)

""" 3. COMBINE PARAMETERS FOR FILES OF THE SAME URL """
# url_num_to_params[i] holds the combined ML parameters of all files whose URL is ID i
url_num_to_params = {}

# url_num_to_params[i] holds the number of files whose URL is ID i. Used for averaging
url_num_to_num_files = {}

for file_number in range(0, len(all_file_url_num)):
	url_num = all_file_url_num[file_number]
	url_num_to_params[url_num] = np.add(url_num_to_params[url_num], all_file_params[file_number]) if url_num in url_num_to_params else np.array(all_file_params[file_number])
	url_num_to_num_files[url_num] = url_num_to_num_files[url_num] + 1 if url_num in url_num_to_num_files else 1

for url_num in range(0, len(url_num_to_params)):
        url_num_to_params[url_num] = url_num_to_params[url_num] / url_num_to_num_files[url_num]


print(3)

""" 4. MACHINE LEARNING TRAINING """
# X is a list with the averaged histograms of each URL. [url_1_avg_histogram, url_2_avg_histogram, ...]
X = np.array([param for param in url_num_to_params.values()])
# Y is all the URL IDs
y = [url_num for url_num in url_num_to_params]

#fit = classifier.fit(X, y)

print(4)

""" 5. MACHINE LEARNING PREDICTION """
# Fit the model on the raw, non-averaged data
actuals, predicted = [], []
for i in range(0, trials):
	print(i)
	X_train, X_test, y_train, y_test = train_test_split(all_file_params, all_file_url_num, random_state = i)
	y_pred = classifier.fit(X_train, y_train).predict(X_test)
	actuals.extend(y_test)
	predicted.extend(y_pred)

print(5)

# Confusion matrix
matrix = confusion_matrix(actuals, predicted)
normalized = matrix.astype('float') / matrix.sum(axis = 1)[:, np.newaxis]
print("\n// Normalized Confusion Matrix")
print(normalized)


print(6)

# Plot the matrix
unique_labels = list(set(all_file_url_num))
def plot_confusion_matrix(cm, title = 'Confusion Matrix', cmap = plt.cm.Blues):
    plt.imshow(cm, interpolation = 'nearest', cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(y))
    plt.xticks(tick_marks, y, rotation = 45)
    plt.yticks(tick_marks, y)
    plt.tight_layout()
    plt.ylabel('Actual')
    plt.xlabel('Predicted')

print("\n// Plotting Externally...\n")
plt.figure()
plot_confusion_matrix(normalized, title = 'Normalized Confusion Matrix')
plt.show()


# Other Potential classifiers
#from sklearn.neighbors import KNeighborsClassifier
#classifier_1 = KNeighborsClassifier(n_neighbors = 1)
#from scipy import spatial
#tree = spatial.KDTree(x)








