import time
import zipfile

import password_cracker.evaluator as evaluator
import password_cracker.train as train
from password_cracker import *


def brute_force_attack(zip_file_path, letter_dic, password_length=-1, destination_path=EXTRACT_TO_PATH):
	"""
	function takes the zip file pointer as an argument. The brute force function will generate all the possibilities,
	and attempt them. It should output the correct password once found.  If successful, return True, otherwise return
	False.

	:param destination_path: the destination path
	:param zip_file_path: the zip file name
	:param letter_dic: the letter dic
	:param password_length: the length of password
	:return: If successful, return True, otherwise return False.
	"""
	with zipfile.ZipFile(zip_file_path, compression=zipfile.ZIP_DEFLATED) as zip_file:
		if password_length <= 0:
			pass
		elif letter_dic.__len__() < password_length:
			return
		else:
			pass
		length_of_side = letter_dic.__len__()
		largest_possible = evaluator.cal_largest_possible_index(password_length, length_of_side)
		start_time = time.time()
		for i in range(1, largest_possible + 1):
			password = evaluator.decode_password(i, letter_dic)
			try:
				zip_file.extractall(destination_path, pwd=bytes(password, "UTF-8"))
				print("password is", password)
				print(
						("Your Password is the {}th permutation of the letter_dic, the total process took {" +
						 "} second").format(i, time.time() - start_time)
				)
				break
			except:
				print("wrong", password)
				continue


def dictionary_attack(zip_file_path, destination_path=EXTRACT_TO_PATH):
	"""
	function takes the zip file pointer and dictionary file pointer as arguments. It should output the correct
	password once found or print an error message if not successful. If successful, return True, otherwise return
	False.

	:param destination_path: the destination of the path
	:param zip_file_path: the zip file pointer
	:return: If successful, return True, otherwise return False.
	"""
	with zipfile.ZipFile(zip_file_path, compression=zipfile.ZIP_DEFLATED) as zip_file:
		start_time = time.time()
		for password in PASSWORD_DICTIONARY:
			try:
				zip_file.extractall(destination_path, pwd=bytes(password, "UTF-8"))
				print("password is", password)
				print("the total process took {} second".format(time.time() - start_time))
				break
			except:
				print("wrong", password)
				continue
		print("Dictionary has used up, try another method!")


def smart_attack(zip_file_path, destination_path=EXTRACT_TO_PATH):
	"""
	function takes the zip file path and, it will load the trained data, if no trained data, use regular brutal force
	attack
	
	the smart attack is a optimised brutal force based on simple machine learning
	
	what does the smart attack do is to use the frequently used password data, and find the most likely, then perform
	expend search around it, this in theory will boost up the search speed.
	
	:param destination_path:
	:param zip_file_path: the zip file path
	:return:
	"""
	# try to load the data base
	trained = train.prepare_trained_data_base(version=1)
	if trained["train_method"] is not "train_one":
		print("Fail to load Trained data")
		return
	# if fail use brutal force
	if trained is None:
		print("Fail to load Trained data, using brutal force")
		brute_force_attack(zip_file_path, DEFAULT_LETTER_BASE)
		return
	else:
		print("Using Trained data base : {}".format(trained["time_stamp"]))
	# fetch the base it used to train and the data
	base = trained["base"]
	data = trained["trained_data"]
	length_of_side = base.__len__()
	# starts from the most frequent dim and then expend
	with zipfile.ZipFile(zip_file_path, compression=zipfile.ZIP_DEFLATED) as zip_file:
		start_time = time.time()
		# 0 : the dim
		# 1 : the length
		# 2 : the mean
		for item in data:
			low_bounds, high_bounds =\
				evaluator.cal_largest_possible_index(item[0] - 1, length_of_side),\
					evaluator.cal_largest_possible_index(item[0], length_of_side)
			left_index = item[2]
			right_index = item[2] + 1
			left_has = True
			# perform expend search around the mean
			while True:
				# if left has then try
				# if not continue, and set left has to False
				if left_index > low_bounds:
					password = evaluator.decode_password(left_index, base)
					try:
						zip_file.extractall(destination_path, pwd=bytes(password, "UTF-8"))
						print("password is", password)
						print("the total process took {} second".format(time.time() - start_time))
						return password
					except:
						# print("wrong", password)
						pass
					left_index -= 1
				else:
					left_has = False
				# if right has then try
				# if not, check left has or not if left not, then break
				if right_index <= high_bounds:
					password = evaluator.decode_password(right_index, base)
					try:
						zip_file.extractall(destination_path, pwd=bytes(password, "UTF-8"))
						print("password is", password)
						print("the total process took {} second".format(time.time() - start_time))
						return password
					except:
						# print("wrong", password)
						pass
					right_index += 1
				else:
					if not left_has:
						break


def smart_attack_2(zip_file_path, destination_path=EXTRACT_TO_PATH):
	# try to load the data base
	trained = train.prepare_trained_data_base(version=2)
	if trained["train_method"] != "train_two":
		print("Fail to load Trained data")
		return
	# if fail use brutal force
	if trained is None:
		print("Fail to load Trained data, using brutal force")
		brute_force_attack(zip_file_path, DEFAULT_LETTER_BASE)
		return
	else:
		print("Using Trained data base : {}".format(trained["time_stamp"]))
	# fetch the base it used to train and the data
	base = trained["base"]
	data = trained["trained_data"]
	# for length, data_base in data:
	print(evaluator.create_weighted_list(length=data[4][0], letter_dic=base, trained=data[4][1]))
	pass


def both_attack():
	"""
	function takes the zip file pointer and dictionary file pointer as arguments. This method perform a combination of
	dictionary attack and brute_force_attack, it will only do brute_force_attack when the dictionary attack fail
	
	:param zip_file: the zip file pointer
	:return: If successful, return True, otherwise return False.
	"""
	pass


def main():
	# smart_attack(
	# 		os.path.join(PATH, "zips", "1544647865.044203.zip")
	# )
	# smart_attack(
	# 		os.path.join(PATH, "zips", "1544648438.169172.zip")
	# )
	smart_attack_2(None)


if __name__ == '__main__':
	main()
