from matplotlib import pyplot as plt
from prettytable import PrettyTable


# ------------- Display ---------------


def plot_primes(primes, bound):
	print(f'All prime numbers smaller than {bound}:\n', primes)


def plot_consol(group_label, groups_len, group):
	tab = PrettyTable()
	tab.field_names = ["Group", "Count", "Total"]

	total = 0
	for label, group_len in zip(group_label, groups_len):
		total += group_len
		tab.add_row([label, group_len, total])

	print('\nAll primes grouped by {}:'.format(group))
	print(tab)


def plot_sorted_curve(group_label, groups_len):
	plt.figure('Prime Numbers')
	plt.plot(group_label, groups_len)
	
	plt.title("Count prime numbers")
	plt.ylabel("Count")
	plt.xlabel("Group")
	plt.show()


def plot_digit_curve(labels, values):
	plt.figure('Prime Numbers')
	plt.bar(labels, values)
	
	plt.title("Count prime numbers by digits")
	plt.ylabel("Count")
	plt.xlabel("Digit")
	plt.show()



def plot_3digit_curve(labels, values):
	plt.figure(figsize=(9, 3))

	plt.title("Count prime numbers by digits")
	plt.ylabel("Count")
	plt.xlabel("Digit")

	for i in range(len(labels)):
		plt.subplot(131 + i)
		plt.bar(labels[i], values[i])

	# plt.figure('Prime Numbers')
	plt.show()