import pdb
import csv
import math
import random
from DecisionTree import DecisionTree


# Global vars
TREES = 100
THRESHOLD = 50
MIN_FEAT = 50
MAX_FEAT = 100

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

train = alldata[:int(len(alldata) / 2)]
test = alldata[int(len(alldata) / 2)]

# Split m into random sub-matrices
# Random columns and data entries
tree_data = []
forest = []
for i in range(TREES):
	temp = []

	# Select the features
	random.shuffle(cols)
	num_cols = random.randrange(MIN_FEAT, MAX_FEAT + 1)
	temp.append(cols[:num_cols + 1])

	# Select random data
	x = random.randrange(0, len(train) - 100)
	y = random.randrange(x, len(train))
	for tweet in train[x:y]:
		person = tweet[0]
		words = tweet[1].split()
		entry = [person] + [1 if c in words else 0 for c in temp[0]]
		temp.append(entry)

	tree_data.append(temp)

# Create / Init. the forest
for data in tree_data:
	forest.append(DecisionTree(data, -1))

for tree in forest:
	tree.buildTree(tree.data)
	tree.execute()

# Run test
correct, wrong = 0, 0
for tweet in test:
	predictions = []
	person = tweet[0]
	words = tweet[1].split()
	for tree in forest:
		entry = [1 if c in words else 0 for c in tree.features]
		predictions.append(tree.predict(entry))

	p = 'HillaryClinton'
	x = predictions.count('HillaryClinton')
	if predictions.count('realDonaldTrump') > x:
		p = 'realDonaldTrump'

	if(p == person):
		correct += 1
	else:
		wrong += 1

print('Correct classifications', correct)
print('Wrong classifications', wrong)
print('Accuracy', correct / (correct + wrong))
