#  -*- coding: utf-8 -*-
import sys
import csv
import math

sys.setrecursionlimit(1500)

class DecisionTree:

	def __init__(self, data, index):
		self.classifier = 'def classify(self, data):'
		self.data = data[1:]
		self.features = data[0]
		self.index = index


	def split(self, data, attribute, remove=False):
		retvals = {}
		allattributes = set([i[attribute] for i in data])
		for d in data:
			c = d[attribute]
			aList = retvals.get(c, [])
			if(remove):
				d.pop(attribute)
			aList.append(d)
			retvals[c] = aList
		return retvals


	def entropy(self, oneclass):
		pos = len([i for i in oneclass if i[0] == 'HillaryClinton'])
		neg = len([i for i in oneclass if i[0] == 'realDonaldTrump'])
		total = pos + neg
		if(min((pos, neg)) == 0):
			return 0
		entropy = -(pos / total) * math.log(pos / total, 2) - (neg / total) * math.log(neg / total, 2)
		return entropy


	def gain(self, oneclass, attribute):
		d = [(self.entropy(i), len(i)) for i in self.split(oneclass, attribute, False).values()]
		nAll = sum([i[1] for i in d])
		gain = sum([(i[0] * i[1]) / nAll for i in d])
		return gain


	def getHighestGain(self, oneclass):
		before = self.entropy(oneclass)
		classes = [i for i in range(0, len(oneclass[0]) - 1)]
		entropies = [self.gain(oneclass, c) for c in classes]
		return entropies.index(min(entropies)) + 1


	def isPure(self, oneclass):
		classes = [i for i in range(1, len(oneclass[0]))]

		for c in classes:
			if(len(set([i[c] for i in oneclass])) > 1 ):
				return False
			return True


	def isEmpty(self, oneclass):
		return len(oneclass[0]) <= 1


	def mostCommon(self, oneclass):
		lst = [i[0] for i in oneclass]
		return max(set(lst), key = lst.count)


	def confidence(self, oneclass):
		mostcommon = self.mostCommon(oneclass)
		return len([i[0] for i in oneclass if i[0] == mostcommon]) / len(oneclass)


	def buildTree(self, oneclass, spaces='   '):
		if(self.isEmpty(oneclass) or self.isPure(oneclass)):
			self.classifier += '\n' + spaces + 'return (' + str(self.mostCommon(oneclass)) + ')\n'
			return

		highest = self.getHighestGain(oneclass)
		d = self.split(oneclass, highest)
		for key, value in d.items():
			# print(spaces, 'if', key)
			self.classifier += '\n' + spaces + 'if(data[' + str(highest) + '] == \"' + str(key) + '\"):'
			self.buildTree(value, spaces + '   ')


	def print_classifier(self):
		print(self.classifier)
		

	def execute(self):
		exec(self.classifier)
	
	def predict(self, data):
		return self.classify(data)

