

def get_digits(primes, place):
	primes_by_digit = ewtract_digits(primes, place)
	return get_len(primes_by_digit)


def ewtract_digits(primes, place):
	digits = {}
	for prime in primes:
		s = str(prime)
		if (len(s) >= place):
			if s[-place] not in digits:
				digits[s[-place]] = []	
			digits[s[-place]] += [prime]

	return digits


def get_len(prime_groups):
	group_label = []
	groups_len = []

	for key, value in prime_groups.items():
		group_label += [key]
		groups_len += [len(value)]

	return group_label, groups_len