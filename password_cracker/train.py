import json
import time

import numpy as np

from password_cracker import *
from password_cracker.evaluator import *


def train(data_base=PASSWORD_DICTIONARY, letter_dic=PASSWORD_BASE):
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
	# calculate the largest basic
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
		"base":         letter_dic,
		"trained_data": trained_data,
	}
	# create the json file
	json_path = os.path.join(DATA_PATH, "trained.json")
	with open(json_path, 'w') as dt:
		json.dump(trained_info, dt, indent=4)


def prepare_trained_data_base():
	"""
	read the trained .json file, and create a dic hold it
	:return: the data base as dic
	"""
	json_path = os.path.join(DATA_PATH, "trained.json")
	if not os.path.isfile(json_path):
		print(json_path)
		return None
	with open(json_path, 'r') as dt:
		data = json.load(dt)
	return data


if __name__ == '__main__':
	train()
