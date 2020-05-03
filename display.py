from matplotlib import pyplot as plt
from prettytable import PrettyTable


# ------------- Display ---------------


def plot_primes(primes, bound):
	print(f'All prime numbers smaller than {bound}:\n', primes)


def plot_consol(group_label, groups_len, group):
	title = f'\nAll primes grouped by {group}:'
	columns_names = ["Group", "Count", "Total"]

	rows = []
	total = 0
	for label, group_len in zip(group_label, groups_len):
		total += group_len
		rows += [label, group_len, total]

	print_table(columns_names, rows, title)


def print_table(columns_names, rows, title):
	tab = PrettyTable()
	tab.field_names = columns_names

	for row in rows:
		tab.add_row(row)

	print(title)
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