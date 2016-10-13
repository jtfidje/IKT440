import pdb

import csv
import math
import random


# Global vars
TREES = 50
THRESHOLD = 10
MIN_FEAT = 2
MAX_FEAT = 10

# Read and extract relevant data
data = [d for d in csv.reader(open('tweets.csv', 'r', encoding='utf8'))]
alldata = [[x[1], x[2]] for x in data[1:]] # Person, Tweet

# Create word-dictionary and count the occurance of each word
dictionary = {}
for tweet in alldata:
	for word in tweet[1].split():
		if word not in dictionary.keys():
			dictionary[word] = 0
		dictionary[word] += 1

print('Dict before threshold:', len(dictionary))	# Print len before applying threshold filter
dictionary = {k: v for k, v in dictionary.items() if v > THRESHOLD}
print('Dict after threshold:', len(dictionary))	# Print len after applying threshold filter

# Create full data matrix from dictionary
cols = list(dictionary.keys())
m = []
for tweet in alldata:
	person = tweet[0]
	words = tweet[1].split()
	entry = [True if c in words else False for c in cols]
	entry.append(person)
	m.append(entry)

# Split m into random sub-matrices
# Random columns and data entries
m_trees = []
random.shuffle(alldata)
for i in range(0, len(m), TREES):
	temp = []

	# Select the features
	random.shuffle(cols)
	num = random.randrange(MIN_FEAT, MAX_FEAT + 1)
	temp.append(cols[:num + 1])

	# Select data
	for tweet in alldata[i:i + TREES]:
		person = tweet[0]
		words = tweet[1].split()
		entry = [True if c in words else False for c in temp[0]]
		entry.append(person)
		temp.append(entry)


	m_trees.append(temp)






