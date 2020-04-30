from matplotlib import pyplot as plt
from prettytable import PrettyTable
    

UPPER_BOUND = 100
GROUP = 10


def main():
	l = prime_numbers(UPPER_BOUND)
	print('All prime numbers less than {}:\n'.format(UPPER_BOUND), l)
	
	map = group_by(l, GROUP)

	prime_groups = digest(map)

	plot_consol(prime_groups)
	plot_curve(prime_groups)
	

def prime_numbers(borne_sup):
	prime_list = []
	for n in range(2, borne_sup):
		for x in range(2, n):
			if n % x == 0:
				break
		else:
			# loop fell through without finding a factor
			prime_list.append(n)

	return prime_list


def group_by(list, group):
	map_group = {}

	i=0
	map_group[i] = []	
	for x in list:
		if x >= (i+1)*group:
			while x >= (i+1)*group:
				i+=1
			map_group[(i)*group] = []
		
		map_group[(i)*group].append(x)

	return map_group


def digest(map):
	l = []
	count = 0
	for k, v in map.items():
		count += len(v)
		l.append(len(v))

	return l


def plot_curve(list):
	plt.figure('Prime Numbers')
	plt.plot(list)
	
	plt.title("count prime numbers")
	plt.ylabel("count")
	plt.xlabel("group")
	plt.show()


def plot_consol(list):
	tab = PrettyTable()

	tab.field_names = ["Group", "Count", "Total"]
	total = 0
	for i, elm in enumerate(list):
		total += elm
		tab.add_row([i*GROUP, elm, total])


	print('\nAll primes grouped by {}:'.format(GROUP))
	print(tab)

# ----------------------------


main()