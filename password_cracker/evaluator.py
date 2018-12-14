"""
Designed to evaluate a string in some base
"""


def evaluate_weight(string: str, letter_dic: list, length, trained):
	"""
	To evaluate the string based on the trained data base (the data base method should be using "train_two")
	
	:param length:
	:param letter_dic:
	:param string:
	:param trained:
	:return:
	"""
	digit_index = 0
	weight = 0
	while digit_index < length:
		weight += trained[digit_index][letter_dic.index(string[digit_index])][1]
		digit_index += 1
	return weight


def create_weighted_list(length, letter_dic: list, trained):
	indexed_list = [0] * length
	weighted_list = []
	while True:
		string = "".join([letter_dic[letter_index] for letter_index in indexed_list])
		weighted_list.append((string, evaluate_weight(string, letter_dic, length, trained)))
		# move to next index
		# if not having next index, that means we are finished
		if not move_to_next_index(length - 1, indexed_list, letter_dic.__len__()):
			break
		print(string)
	weighted_list.sort(key=lambda pair: pair[1], reverse=True)
	return weighted_list


def move_to_next_index(checking_index, indexed_list, max_length):
	value = indexed_list[checking_index]
	# if can have next index then add one
	if value + 1 < max_length:
		indexed_list[checking_index] += 1
		return True
	else:
		if checking_index == 0:
			return False
		# clear the buffer, then move to previous level
		indexed_list[checking_index] = 0
		return move_to_next_index(checking_index - 1, indexed_list, max_length)


def decode_password(index: int, letter_dic: list):
	"""
	to decode a specific index to the letter inside a letter_dic, and feed with the letter dic

	:param index: the index that trying to find (the index must be illegible, the index should be in range of
	(1 &lt;= index &lt;= max_possible)
	:param letter_dic: the letter dic is using
	:return: a string that has decoded
	"""
	return "".join([str(letter_dic[index]) for index in find_dimension(index, letter_dic.__len__())[::-1]])


def encode_password(password: str, letter_dic: list):
	"""
	to encode a specific password to a integer representative, in the base of letter_dic, in another word, to
	get the index of the string that lays on the letter_dic base, one of the credential it follows is that
	it is going to have the same things in the same base, with the same value for decode and encode if you do
	something like:

	some_base = ['q','w','e'...]
	decode_password(encode_password("qwe", some_base), some_base)

	should exactly return "qwe" as it takes in

	:param password: the password to encode
	:param letter_dic: the letter_dic
	:return: the integer representative(index) which is greatest or equals to 1, in the base given
	"""
	# get all the chars in the string
	password_chars = list(password)[::-1]
	# start a buffer for indexes
	indexes = []
	# iter through the password
	for char in password_chars:
		# if the char is in the base, then find the index of it, then push into the buffer
		# else it raise an RuntimeError
		if char in letter_dic:
			index = letter_dic.index(char)
			indexes.append(index)
		else:
			print(char)
			raise RuntimeError("Encoding Error : char not in the letter_dic")
	num_of_dimension = indexes.__len__()
	length_of_side = letter_dic.__len__()
	# accumulate the index, calculate all previous dimensions index and added it to the index
	index = cal_largest_possible_index(num_of_dimension - 1, length_of_side)
	# now all previous dimension is handled, we need to work on the current dimension
	# start a iteration on every dimension till the 1st dimension,
	dim = num_of_dimension - 1
	while dim > 0:
		index += (indexes[dim]) * (length_of_side ** dim)
		dim -= 1
	else:
		index += indexes[dim] + 1
	return index


def cal_num_of_dimension(index, length_of_side):
	# first start a buffer to accumulate the dimension
	num_of_dimension = 0
	# start a infinity loop until we find the desired dimension
	while True:
		# if the item is still exist in the next dimension then continue
		# else then we got the dimension
		# Note: if a index is 0 on the dimension that means it falls on the last of the previous dimension
		if index > length_of_side ** (num_of_dimension + 1):
			num_of_dimension += 1
		else:
			num_of_dimension += 1
			break
		# decrease by the item of dimension
		index -= length_of_side ** num_of_dimension
	return num_of_dimension


def find_dimension(index, length_of_side):
	"""
	to locate the index and returns a vector that points to such index (find which dimension it is on and which place
	in such dimension

	Note: please note that, in this evaluating system, every string should in theory has a distinct indexes

	:param index: the index that trying to find (the index must be illegible, the index should be in range of
	(1 &lt;= index &lt;= max_possible)
	:param length_of_side: the length of the side (the letter dic length)
	:return: a vector that points to the index
	"""
	num_of_dimension = cal_num_of_dimension(index, length_of_side)
	# the reminder we got is actually indicate the distance from the origin of that dimension to the point
	vector = [0] * num_of_dimension
	# to start a index of number of dimension as we iter through the dimension
	dim = num_of_dimension - 1
	# have a reminder to record the left over
	reminder = index
	# start a loop that iter thought every dimension
	while dim >= 0:
		# to calculate the max value is held in this dimension
		num_in_this_dim = length_of_side ** dim
		# to peal off the value and get which value is on
		value_in_this_dim = reminder // num_in_this_dim
		# to store the value inside the reminder
		vector[dim] = value_in_this_dim - 1
		# to calculate the reminder again for the next dimension
		reminder = reminder % num_in_this_dim
		# move to the next dimension
		dim -= 1
	return vector


def cal_largest_possible_index(length, length_of_side):
	"""
	calculate the largest possible number inside that could be reached with such length and length of side

	:param length: the letter_dic length
	:param length_of_side: the length of the side (the letter dic length)
	:return: the largest possible number
	"""
	largest_possible = 0
	for i in range(1, length + 1):
		largest_possible += length_of_side ** i
	return largest_possible
