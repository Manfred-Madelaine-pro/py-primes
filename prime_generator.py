from pathlib import Path



# ------------- Generatoe ---------------


def get_prime_numbers(upper_bound):
	prime_list = []
	for n in range(2, upper_bound):
		for x in range(2, n):
			if n % x == 0:
				break
		else:
			prime_list += [n]

	return prime_list



# ------------- File ---------------


CSV = 'csv'
FILE = 'file'
DATABASE = 'database'

OUTPUT_PATH = "output/"


def load(file_name):
	lines = []
	with open(file_name, 'r') as file:
		lines = [int(current_place.rstrip()) for current_place in file.readlines()]

	return lines


def save(list, type, name=None):
	if(not name):
		name = 'output_' + get_date_timestamp()

	if type == FILE:
		return write_in_file(list, name)
	elif type == DATABASE:
		pass


def get_date_timestamp():
	dt = str(datetime.datetime.now()) # example : 2020-04-29 23:12:05.033586
	dt = dt.replace(' ', '_')
	dt = dt.replace(':', '')		# remove time token
	dt = dt.split('.')[0] 			# remove nano second
	return dt


def write_in_file(list, file_name):
	# make sure that the output directory exists 
	Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

	f_name = f"{OUTPUT_PATH}{file_name}.txt"
	with open(f_name, 'w') as file:
		file.writelines(f"{elm}\n" for elm in list)

	return f_name


def write_in_csv(list, file_name):
	with open(file_name + '.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['group', 'count']) # column name
		for _, v in enumerate(list):
			writer.writerow([_, v])




# ----------------------- Database ---------------------------



# ----------------------- Test ---------------------------


def test_write_and_read_file():
	name = write_in_file([i for i in range(3)], 'test')
	print(load(name))
	print(name)

# test_write_and_read_file()