import timeit
from statistics import mean

import display as dp
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
	# 0: {SHORT: 'Many to Many', LONG: 'Create and access many time'},
	1: {SHORT: 'One to Many (file)', LONG: 'Create once, access many times from file'},
	2: {SHORT: 'One to Many (DB)', LONG: 'Create once, access many times from database'},
}

BOUND = 20
GROUP = BOUND/10

BATCH    = 100
REPEAT   = 5
NUMBER   = 5

REPEAT_C   = 1
NUMBER_C   = 1



# ----------------------- Timer ---------------------------

def creating_perfs():
	tested_func = wrapper(create_primes, BOUND)
	raw_stats = timeit.repeat(tested_func, repeat=REPEAT_C, number=NUMBER_C)

	data = digest(raw_stats)
	print(f'\n{data}\n')


def storing_perfs():
	data = {}
	for test_id in ALL_TESTS.keys():
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



# ----------------------- Create ---------------------------

def create_primes(bound):
	print('.', end = '', flush=True)
	p = pg.get_prime_numbers(bound)
	print(f'{p}')


# ----------------------- Store ---------------------------

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
		primes = pg.get_prime_numbers(bound)
		file_name = pg.save(primes, 'file', name=NAME)

	primes = pg.load(file_name)
	ps.sort_primes(primes, group)


def create_once_and_access_many_db(bound, group, index): # db
	db_name = f'database/{NAME}.db'
	prime_db = pg.access_db(db_name)
	
	if(index == 0):
		primes = pg.get_prime_numbers(bound)
		pg.populate_db(prime_db, primes)

	primes = pg.load_db(prime_db)
	prime_db.close()
	
	ps.sort_primes(primes, group)



# ----------------------- Stats ---------------------------

def digest(raw_stats):
	stats = {}
	raw_stats.sort()
	stats[BEST] = raw_stats[0]
	stats[WORST] = raw_stats[-1]
	stats[AVERAGE] = mean(raw_stats)
	stats[ALL] = raw_stats

	return stats
	

def compare_stats(data):
	stats = []
	col = [NAME, BEST, AVERAGE, WORST]
	indexes = list(ALL_TESTS.keys())
	for i, stat in enumerate(data):
		idx = indexes[i]
		name = ALL_TESTS[idx][SHORT]
		best = data[idx][BEST]
		avg = data[idx][AVERAGE]
		worst = data[idx][WORST]

		stats += [[name, best, avg, worst]]

	dp.print_table(col, stats, "All Performance Tests")



# ----------------------- Test ---------------------------

def test_db():
	for i in range(10):
		create_once_and_access_many_db(BOUND, GROUP, i)



# ----------------------- Main ---------------------------

# storing_perfs()
creating_perfs()