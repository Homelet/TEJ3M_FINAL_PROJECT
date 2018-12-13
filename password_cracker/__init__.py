import os


DEFAULT_LETTER_BASE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
	't', 'u', 'v', 'w', 'x', 'y', 'z']
"""
The letter base or letter_dic is a list distinct characters, and all calculation must have a same base,
a index of a same string in different base is different
"""
RANDOM_ZIP_CONTENT = "# this is a random file that needs to be compressed into a zip, the password is randomly "\
					 "assigned\npassword : "
"""
This is the random content inside the zipfile
"""

PATH = os.path.split(os.path.abspath(__file__))[0]
"""
The path of the current working directory
"""

PASSWORD_DATA_BASE_DIC = os.path.join(PATH, "data", "password_base.txt")
"""
The path of the password data base
"""

EXTRACT_TO_PATH = os.path.join(PATH, "EXTRACT_TO")

DATA_PATH = os.path.join(PATH, "data")


def create_password_database():
	"""
	function does not take in any arguments and should return a file pointer to the dictionary file. It should keep
	re-prompting the user if the file doesnt exist.

	:return: the list contains all password
	"""
	with open(PASSWORD_DATA_BASE_DIC, 'r', encoding='UTF-8') as password_database:
		password_data_text = password_database.read()
		password_dictionary = password_data_text.split('\n')
		password_base = list(set(password_data_text.replace('\n', '').replace(' ', '')))
		password_base.sort()
	return password_dictionary, password_base


PASSWORD_DICTIONARY, PASSWORD_BASE = create_password_database()
