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

ALL_STORING_TESTS = {
	0: {SHORT: 'Many to Many', LONG: 'Create and access many time'},
	1: {SHORT: 'One to Many (file)', LONG: 'Create once, access many times from file'},
	2: {SHORT: 'One to Many (DB)', LONG: 'Create once, access many times from database'},
}

VERSION_1 = 'v1'
VERSION_2 = 'v2'

ALL_CREATING_TESTS = [
	VERSION_1,
	VERSION_2
]

POTENTIAL_ITER = 'Potential'
EFFECTIVE_ITER = 'Reality'



BOUND = 1000
GROUP = BOUND/10

BATCH    = 100
REPEAT   = 5
NUMBER   = 5

REPEAT_C   = 5
NUMBER_C   = 5


GLOBAL_STATS = {}


# ----------------------- Timer ---------------------------

def creating_perfs():
	data = {}
	for i in range(len(ALL_CREATING_TESTS)):
		tested_func = wrapper(create_primes, BOUND, ALL_CREATING_TESTS[i])
		raw_stats = timeit.repeat(tested_func, repeat=REPEAT_C, number=NUMBER_C)

		data[i] = digest(raw_stats)
		print(f'\n{data[i]}\n')

	# compare best and worse times
	compare_stats(data, ALL_CREATING_TESTS)
	# curve
	plot_stats(GLOBAL_STATS)


def storing_perfs():
	data = {}
	for test_id in ALL_STORING_TESTS.keys():
		print(f'{ALL_STORING_TESTS[test_id][LONG]:^50}')

		tested_func = wrapper(run_batch, BOUND, GROUP, test_id, BATCH)

		raw_stats = timeit.repeat(tested_func, repeat=REPEAT, number=NUMBER)
		data[test_id] = digest(raw_stats)

		print(f'\n{data[test_id]}\n')

	# compare best and worse times
	tests_name = [test[SHORT] for _, test in ALL_STORING_TESTS.items()]
	compare_stats(data, tests_name)
	

'''
Needed to time a Python function with arguments
'''
def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped



# ----------------------- Create ---------------------------

def create_primes(bound, test):
	print('.', end = '', flush=True)
	p, stats = pg.get_prime_numbers(bound, test, with_stats=True)

	GLOBAL_STATS[test] = stats


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
	

def compare_stats(data, tests_name):
	stats = []
	col = [NAME, BEST, AVERAGE, WORST]
	for idx, stat in enumerate(data):
		name = tests_name[idx]
		best = data[idx][BEST]
		avg = data[idx][AVERAGE]
		worst = data[idx][WORST]

		stats += [[name, best, avg, worst]]

	dp.print_table(col, stats, "All Performance Tests")
	faster(VERSION_1, data[0][AVERAGE], VERSION_2, data[1][AVERAGE])


def faster(old_name, old, new_name, new):
	percent = old/new
	print(f"Average : function '{new_name}' is {percent:.1%} faster than '{old_name}'.")


def plot_stats(data):
	c1_v1 = data[VERSION_1][POTENTIAL_ITER]
	c1_v2 = data[VERSION_2][POTENTIAL_ITER]
	c1_values = [c1_v1, c1_v2]

	c2_v1 = data[VERSION_1][EFFECTIVE_ITER]
	c2_v2 = data[VERSION_2][EFFECTIVE_ITER]
	c2_values = [c2_v1, c2_v2]


	abscisse = [x for x in range(len(c1_v1))]
	dp.plot_2_curves(abscisse, c1_values, POTENTIAL_ITER, c2_values, EFFECTIVE_ITER)
	

# ----------------------- Test ---------------------------

def test_db():
	for i in range(10):
		create_once_and_access_many_db(BOUND, GROUP, i)



# ----------------------- Main ---------------------------

creating_perfs()
# storing_perfs()