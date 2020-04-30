from matplotlib import pyplot as plt
from prettytable import PrettyTable
    

UPPER_BOUND = 200
GROUP = 10


def main():
	primes = get_prime_numbers(UPPER_BOUND)

	prime_groups = group_by(primes, GROUP)

	group_label, groups_len = get_len(prime_groups)

	plot_primes(primes)
	plot_consol(group_label, groups_len)
	plot_curve(group_label, groups_len)

	
def get_prime_numbers(upper_bound):
	prime_list = []
	for n in range(2, upper_bound):
		for x in range(2, n):
			if n % x == 0:
				break
		else:
			prime_list += [n]

	return prime_list


'''
	Devide the intervalle into smaller intervalles with the size of "group".
	Regroup the primes, based on those sub-intervalles.
'''
def group_by(primes, group):
	i=0
	map_group = {}
	map_group[i] = []	

	for p in primes:
		if p >= (i+1)*group:
			while p >= (i+1)*group:
				i+=1
			map_group[(i)*group] = []
		
		map_group[(i)*group] += [p]

	return map_group


def get_len(prime_groups):
	group_label = []
	groups_len = []

	for key, value in prime_groups.items():
		group_label += [key]
		groups_len += [len(value)]

	return group_label, groups_len


# ------------- Display ---------------


def plot_primes(primes):
	print(f'All prime numbers smaller than {UPPER_BOUND}:\n', primes)


def plot_consol(group_label, groups_len):
	tab = PrettyTable()
	tab.field_names = ["Group", "Count", "Total"]

	total = 0
	for label, group_len in zip(group_label, groups_len):
		total += group_len
		tab.add_row([label, group_len, total])

	print('\nAll primes grouped by {}:'.format(GROUP))
	print(tab)


def plot_curve(group_label, groups_len):
	plt.figure('Prime Numbers')
	plt.plot(group_label, groups_len)
	
	plt.title("Count prime numbers")
	plt.ylabel("Count")
	plt.xlabel("Group")
	plt.show()


# ------------- Main ---------------


main()