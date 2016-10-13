import csv
import math
import random


# Global vars
TREES = 50
THRESHOLD = 10

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

print(len(dictionary))	# Print len before applying threshold filter
dictionary = {k: v for k, v in dictionary.items() if v > THRESHOLD}
print(len(dictionary))	# Print len after applying threshold filter

# Create full data matrix from dictionary
cols = dictionary.keys()
m = []
for tweet in alldata:
	person = tweet[0]
	words = tweet[1].split()
	entry = [True if c in words else False for c in cols]
	entry.append(person)
	m.append(entry)

# Randomly split m into n number of sublists
random.shuffle(m)
n = int(len(m) / TREES)
m_forest = [m[i:i + n] for i in range(0, len(m), n)]
print(len(m_forest))