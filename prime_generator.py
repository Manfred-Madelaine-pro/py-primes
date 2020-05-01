

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

def write():
	f_name = 'output_' + get_date_timestamp()

	write_in_file(list, f_name)
	# write_in_csv(list, f_name)

	return f_name


def get_date_timestamp():
	dt = str(datetime.datetime.now()) # example : 2020-04-29 23:12:05.033586
	dt = dt.replace(' ', '_')
	dt = dt.replace(':', '')		# remove time token
	dt = dt.split('.')[0] 			# remove nano second
	return dt


def write_in_file(list, f_name):
	f = open(f_name + ".txt", "w")
	f.write("Woops! I have deleted the content!")
	f.close()


def write_in_csv(list, ):
	f = open(f_name + '.csv', 'w')
	with f:
		writer = csv.writer(f)
		writer.writerow(['group', 'count']) # column name
		for _, v in enumerate(list):
			writer.writerow([_, v])
