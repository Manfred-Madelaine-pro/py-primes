import timeit
from statistics import mean


import prime_sorter as ps
import prime_generator as pg


NAME = 'perf_test'

ALL = 'all_times'
BEST = 'best'
WORST = 'worst'
AVERAGE = 'average'

SHORT = 'short'
LONG = 'long'

ALL_TESTS = {
	0: {SHORT: 'Many to Many', LONG: 'Create and access many time'},
	1: {SHORT: 'One to Many (file)', LONG: 'Create once, access many times from file'},
	2: {SHORT: 'One to Many (DB)', LONG: 'Create once, access many times from database'},
}

BOUND = 1000
GROUP = BOUND/10

BATCH    = 30
REPEAT   = 5
NUMBER   = 5


def perfs():
	data = {}
	for test_id in range(len(ALL_TESTS)):
		print(f'{ALL_TESTS[test_id][LONG]:^50}')

		tested_func = wrapper(run_batch, BOUND, GROUP, test_id, BATCH)

		raw_stats = timeit.repeat(tested_func, repeat=REPEAT, number=NUMBER)
		data[test_id] = digest(raw_stats)

		print(f'\n{data[test_id]}\n')

	# compare best and worse times
	compare_stats(data)
	

'''
Needed to time a Python function with arguments
'''
def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def run_batch(bound, group, test_id, batch):
	for i in range(batch):
		if i%(batch/2) == 0:
			print('.', end = '', flush=True)
	
		if(test_id == 0):
			create_and_access_many(bound, group)

		elif(test_id == 1):
			create_once_and_access_many(bound, group, i)

		elif(test_id == 2):
			create_once_and_access_many_db(bound, group, i)


def create_and_access_many(bound, group):
	# create
	primes = pg.get_prime_numbers(bound)
	# access
	ps.sort_primes(primes, group)


def create_once_and_access_many(bound, group, index): # files
	file_name = f'output/{NAME}.txt'
	
	if(index == 0):
		# create
		primes = pg.get_prime_numbers(bound)
		file_name = pg.save(primes, 'file', name=file_name)

	primes = pg.load(file_name)
	ps.sort_primes(primes, group)


def create_once_and_access_many_db(bound, group, index): # db
	db_name = f'database/{NAME}.db'
	prime_db = pg.access_db(db_name)
	
	if(index == 0):
		# create
		primes = pg.get_prime_numbers(bound)
		pg.populate_db(prime_db, primes)

	# rows = pg.load_db(prime_db)
	prime_db.close()
	ps.sort_primes(primes, group)



def digest(raw_stats):
	stats = {}
	raw_stats.sort()
	stats[BEST] = raw_stats[0]
	stats[WORST] = raw_stats[-1]
	stats[AVERAGE] = mean(raw_stats)
	stats[ALL] = raw_stats

	return stats
	

def compare_stats(data):
	percent_b = data[1][BEST]/data[0][BEST]
	percent_w = data[1][WORST]/data[0][WORST]
	percent_a = data[1][AVERAGE]/data[0][AVERAGE]

	print(f"Best : function '{ALL_TESTS[1][SHORT]}' is {percent_b:.1%} faster than '{ALL_TESTS[0][SHORT]}'.")
	print(f"Average : function '{ALL_TESTS[1][SHORT]}' is {percent_a:.1%} faster than '{ALL_TESTS[0][SHORT]}'.")
	print(f"Worst : function '{ALL_TESTS[1][SHORT]}' is {percent_w:.1%} faster than '{ALL_TESTS[0][SHORT]}'.")

# perfs()

for i in range(1,10):
	create_once_and_access_many_db(BOUND, GROUP, i)