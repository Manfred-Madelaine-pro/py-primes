from pathlib import Path

import database as db


POTENTIAL_ITER = 'Potential'
EFFECTIVE_ITER = 'Reality'
TOTAL_ITER = 'Total'


# ------------- Generator ---------------

def get_prime_numbers(upper_bound, version='v2', with_stats=False):
	stats = {
		POTENTIAL_ITER: [],
		EFFECTIVE_ITER: [],
		TOTAL_ITER: 0
	}

	prime_list = []
	for n in range(2, upper_bound):
		count = 0
		searching_list = get_searching_list(version, prime_list, n)
		
		for x in searching_list:
			count += 1

			if n % x == 0:
				break
		else:
			prime_list += [n]

		stats[POTENTIAL_ITER] += [len(searching_list)] 
		stats[EFFECTIVE_ITER] += [count]
		stats[TOTAL_ITER] += count

	if with_stats:
		return prime_list, stats
	return prime_list 


def get_searching_list(version, prime_list, max):
	full_range = range(2, max)
	
	if not prime_list or version == 'v1':
		return full_range 

	shorten_range = prime_list + [x for x in range (prime_list[-1]+1, max)]
	return shorten_range


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

def access_db(db_name):
	return db.get_connection(db_name)


def populate_db(db_connection, list):
	db.create_table(db_connection)

	# convert list elements to tuple
	rows = [(elm,) for elm in list]

	db.insert_rows(db_connection, rows)


def load_db(db_connection):
	rows = db.get_all_primes(db_connection)

	primes = []
	for row in rows:
		primes += [row['primes']]

	return primes



# ----------------------- Test ---------------------------

def test_write_and_read_file():
	name = write_in_file([i for i in range(3)], 'test')
	print(load(name))
	print(name)


def test_write_and_read_db():
	db_name = 'database/test.db'
	prime_db = access_db(db_name)
	
	# create
	primes = [i for i in range(5)]
	populate_db(prime_db, primes)
	prime_db.close()

	# access
	prime_db = access_db(db_name)
	rows = load_db(prime_db)
	prime_db.close()


def test_get_prime_numbers():
	get_prime_numbers(10)


# test_write_and_read_file()
# test_write_and_read_db()
# test_get_prime_numbers()