import json
import time

import numpy as np

from password_cracker import *
from password_cracker.evaluator import *


def train_one(data_base=PASSWORD_DICTIONARY, letter_dic=PASSWORD_BASE):
	"""
	To train the data:
	-> First find which dimension of password is most likely
	-> Then find the mean in each dimension
	
	Then create an .json file to store such trained data
	:return: None
	"""
	# evaluate all strings and put it in a list
	train_base = [encode_password(password, letter_dic) for password in data_base]
	# sort all evaluated values
	train_base.sort()
	length_of_side = letter_dic.__len__()
	# start a index for iter
	index = 0
	# start accumulate the dimensions starts at 1
	dim = 1
	# initialize the max_index possible in current dim
	max_index_in_dim = cal_largest_possible_index(dim, length_of_side)
	# a buffer for storing the processed data
	classified_data = []
	# a secondary buffer for storing local data
	data_in_range = []
	local_data_wrap = (dim, data_in_range)
	# start the loop
	while index < train_base.__len__():
		# get the current data pointed to
		item = train_base[index]
		# if the item is smaller than the index, then it is in range
		# add it to the local buffer
		# if not means this dim is over,
		# add the local buffer to the buffer, and clear the local buffer
		# move to next dim, and calculate the largest in that dim
		if item <= max_index_in_dim:
			data_in_range.append(item)
			index += 1
		else:
			classified_data.append(local_data_wrap)
			data_in_range = []
			dim += 1
			local_data_wrap = (dim, data_in_range)
			max_index_in_dim = cal_largest_possible_index(dim, length_of_side)
	else:
		classified_data.append(local_data_wrap)
	
	# compute the data
	# the data include the length and the rounded mean of the dim
	trained_data = [
		(
			local_data[0],
			local_data[1].__len__(),
			int(np.round(np.mean(local_data[1], dtype=np.float64)))
		)
		for local_data in classified_data if local_data[1].__len__() is not 0
	]
	trained_data.sort(key=lambda it: it[1], reverse=True)
	# create the trained info
	trained_info = {
		"time_stamp":   time.time(),
		"train_method": "train_one",
		"base":         letter_dic,
		"trained_data": trained_data,
	}
	# create the json file
	json_path = os.path.join(DATA_PATH, "trained_v1.json")
	with open(json_path, 'w') as dt:
		json.dump(trained_info, dt, indent=4)


def train_two(data_base=PASSWORD_DICTIONARY, letter_dic=PASSWORD_BASE):
	"""
	train_two is another way of the training process
	the idea of this training is as follow:
	-> first get the most frequently used password length
	-> then get calculate the weight inside each digit along that length only
	
	:param data_base:
	:param letter_dic:
	:return:
	"""
	# first we need to sort it by it's length
	data_base.sort(key=lambda st: st.__len__())
	# first we need to sort the data by it's length
	# start a index for iter
	index = 0
	# a buffer for storing the processed data
	classified_data = []
	# a secondary buffer for storing local data
	data_in_range = []
	# length of password
	length = 1
	# the data wra
	local_data_wrap = (length, data_in_range)
	# start the loop
	while index < data_base.__len__():
		# get the current data pointed to
		item = data_base[index]
		# if the item is smaller than the index, then it is in range
		# add it to the local buffer
		# if not means this dim is over,
		# add the local buffer to the buffer, and clear the local buffer
		# move to next dim, and calculate the largest in that dim
		if item.__len__() == length:
			data_in_range.append(item)
			index += 1
		else:
			classified_data.append(local_data_wrap)
			data_in_range = []
			length += 1
			local_data_wrap = (length, data_in_range)
	else:
		classified_data.append(local_data_wrap)
	# now we have classify all length out, now we need to sort it
	classified_data.sort(key=lambda src: src[1].__len__(), reverse=True)
	# password base length
	base_length = letter_dic.__len__()
	# since the data has been sorted
	# we need to calculate the weight for each character in each digit
	# start a buffer to store data
	weighted = []
	# start the
	for digit_length, local_data in classified_data:
		# [(digit_length, [[[index_in_list, weight], ... ]: index_by_digit, ...]), ...]
		# the first stores the digit
		# the second is the list
		# the third is the digit index
		# the fourth is each value in (index, weight) pair
		weighted_list = (digit_length, [[[i, 0] for i in range(base_length)] for _ in range(digit_length)])
		# to perform the range on every digit
		for digit in range(digit_length):
			# to iter though the data for every digit
			for raw in local_data:
				# get the letter
				letter = raw[digit]
				# if letter in dic then accumulate it
				# if not raise a RuntimeError
				if letter in letter_dic:
					weighted_list[1][digit][letter_dic.index(letter)][1] += 1
				else:
					raise RuntimeError("Training Error : char not in the letter_dic")
		# local_data_size = float(local_data.__len__())
		# calculate the weight inside each range
		# fixme please note that, we are expecting there are about 0.0000000000000001 fluctuation
		# because we couldn't represent the float exactly,
		# for i in range(base_length):
		# 	local_accumulate = weighted_list[1][digit][i][1]
		# 	weighted_list[1][digit][i][1] = local_accumulate / local_data_size if local_accumulate > 0 else 0.0
		# weighted_list[1][digit].sort(key=lambda pair: pair[1], reverse=True)
		# append it to the list
		weighted.append(weighted_list)
	trained_info = {
		"time_stamp":   time.time(),
		"train_method": "train_two",
		"base":         letter_dic,
		"trained_data": weighted,
	}
	# create the json file
	json_path = os.path.join(DATA_PATH, "trained_v2.json")
	with open(json_path, 'w') as dt:
		json.dump(trained_info, dt, indent=4)


def prepare_trained_data_base(version=2):
	"""
	read the trained .json file, and create a dic hold it
	:return: the data base as dic
	"""
	json_path = os.path.join(DATA_PATH, "trained_v" + str(version) + ".json")
	if not os.path.isfile(json_path):
		print("Fail to detect data_base on path :", json_path)
		return None
	with open(json_path, 'r') as dt:
		data = json.load(dt)
	return data


if __name__ == '__main__':
	# train_one()
	train_two()
