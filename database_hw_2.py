import os
import pandas as pd
import numpy as np
import csv
import time

class FileSettings(object):
	def __init__(self, file_name, row_size=100000):
		self.file_name = file_name
		self.row_size = row_size

class FileSplitter(object):
	def __init__(self, file_settings):
		self.file_settings = file_settings
		self.df = pd.read_csv(self.file_settings.file_name, chunksize = self.file_settings.row_size)

	def run(self, directory="temp"):
		try:os.makedirs(directory)
		except Exception as e:pass

		counter = 0
		while True:
			try:
				file_name = "{}/{}_{}_row_{}.csv".format(directory, self.file_settings.file_name.split(".")[0], counter, self.file_settings.row_size)
				df = next(self.df).to_csv(file_name)
				counter = counter + 1
			except StopIteration:
				break
			except Exception as e:pass
		return True

class Node:
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.next = None

class HashTable:
	def __init__(self):
		self.capacity = INITIAL_CAPACITY
		self.size = 0
		self.buckets = [None]*self.capacity
	def hash(self, key):
		hashsum = 0
		for idx, c in enumerate(str(key)):
			hashsum += (idx + len(str(key))) ** ord(c)
			hashsum = hashsum % self.capacity
		return hashsum
	def insert(self, key, value):
		self.size += 1
		index = self.hash(key)
		node = self.buckets[index]
		if node is None:
			self.buckets[index] = Node(key, value)
			return
		prev = node
		while node is not None:
			prev = node
			node = node.next
		prev.next = Node(key, value)
	def find(self, key):
		index = self.hash(key)
		node = self.buckets[index]
		while node is not None and node.key != key:
			node = node.next
		if node is None:
			return None
		else:
			return node.value
	def remove(self, key):
		index = self,hash(key)
		node = self.buckets[index]
		while node is not None and node.key != key:
			prev = node
			node = node.next
		if node is None:
			return None
		else:
			self.size -= 1
			result = node.value
			if prev is None:
				node = None
			else:
				prev.next = prev.next.next
			return result
	
def merge_sort(arr):
	if len(arr) > 1:
		left_arr = arr[:len(arr)//2]
		right_arr = arr[len(arr)//2:]

		merge_sort(left_arr)
		merge_sort(right_arr)

		i=0
		j=0
		merge_ind = 0

		while i < len(left_arr) and j < len(right_arr):
			if left_arr[i][26] < right_arr[j][26]:
				arr[merge_ind] = left_arr[i]
				i += 1
			else:
				arr[merge_ind][26] = right_arr[j][26]
				j += 1
			merge_ind += 1
		
		while i < len(left_arr):
			arr[merge_ind] = left_arr[i]
			i += 1
			merge_ind += 1

		while j < len(right_arr):
			arr[merge_ind] = right_arr[j]
			j += 1
			merge_ind += 1
	return arr

def find():
	for i in range(12):
		file_name = "temp/dataset_" + str(i) + "_row_100000.csv"
		with open(file_name, encoding="utf8") as csvDataFile:
			csvReader = csv.reader(csvDataFile)
			for row in csvReader:
				if row[26] == "Sandman: Dream Hunters 30th Anniversary Edition":
					return

def main():

	helper = FileSplitter(FileSettings(file_name = 'dataset.csv', row_size = 100000))
	helper.run()

	table = HashTable()
	results = []
	for i in range(12):
		results = []
		file_name = "temp/dataset_" + str(i) + "_row_100000.csv"

		with open(file_name, encoding="utf8") as csvDataFile:
			csvReader = csv.reader(csvDataFile)

			for row in csvReader: # each row is a list
				results.append(row)

				table.insert(row[26], row[26])
			sorted = merge_sort(results)
			pd.DataFrame(sorted).to_csv("temp/dataset_" + str(i) + "_row_100000_sorted.csv")

	print("linear Search: ", end = '')
	start = time.time()
	find()
	end = time.time()
	total = end - start
	print(round(total, 20))

	#hash
	print("Hash: ", end = '')
	start = time.time()
	num = table.find("Sandman: Dream Hunters 30th Anniversary Edition")
	end = time.time()
	total = end - start
	print(round(total, 20))

INITIAL_CAPACITY = 100000 * 12
main()
