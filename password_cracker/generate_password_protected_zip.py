"""
To generate password protected zip file for testing purpose
"""
import pyminizip as minizip
import random
import time

from password_cracker import *


def generate_password_zip(path: str, zip_destination: str, password: str, compress_level: int = 5):
	"""
	generate a zip file to the zip_destination with whatever the path variable is pointing to, with the password
	applied
	
	:param path: the path to zip
	:param zip_destination: the destination of zip file
	:param password: the password
	:param compress_level: the compress level, default 5 (1~9, as faster to compressed)
	:return: True if success, else False
	"""
	minizip.compress(path, None, zip_destination, password, compress_level)


def generate_random_password(test_base, password_max_length):
	dimension = random.randint(1, password_max_length)
	string = [None] * dimension
	for i in range(dimension):
		string[i] = random.choice(test_base)
	return "".join(string)


def generate_zips(number_of_zip, letter_dic, max_password_length=8, path_of_zips="zips", path_of_temps="temps"):
	"""
	generate the numbers of zip to test the algorithm
	
	:param path_of_temps:
	:param path_of_zips:
	:param max_password_length: the maximum password length
	:param letter_dic: the letter base or letter dic
	:param number_of_zip: the number of zip needed
	:return:
	"""
	path_of_zips = os.path.join(PATH, path_of_zips)
	path_of_temps = os.path.join(PATH, path_of_temps)
	for _ in range(number_of_zip):
		temp_file_name = str(time.time())
		with open(os.path.join(path_of_temps, temp_file_name + ".txt"), "x", encoding='UTF-8') as temp_file:
			random_password = generate_random_password(letter_dic, max_password_length)
			temp_file.write(RANDOM_ZIP_CONTENT + random_password)
		generate_password_zip(os.path.join(path_of_temps, temp_file_name + ".txt"),
							  os.path.join(path_of_zips, temp_file_name + ".zip"), random_password)


if __name__ == '__main__':
	generate_zips(1, PASSWORD_BASE, max_password_length=8)
