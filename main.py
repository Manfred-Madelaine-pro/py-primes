
import prime_generator as pg
import prime_sorter as ps
import prime_digits as pd

import display as dp


UPPER_BOUND = 1000
GROUP = 100


def main():
	# sorter()
	# units()
	units3()




def sorter():
	primes = pg.get_prime_numbers(UPPER_BOUND)
	labels, values = ps.sort_primes(primes, GROUP)

	dp.plot_primes(primes, UPPER_BOUND)
	dp.plot_consol(labels, values, GROUP)
	dp.plot_sorted_curve(labels, values)


def units():
	place = 1
	primes = pg.get_prime_numbers(UPPER_BOUND)
	labels, values = pd.get_digits(primes, place)
	
	dp.plot_primes(primes, UPPER_BOUND)
	dp.plot_consol(labels, values, 'Digit')
	dp.plot_digit_curve(labels, values)


def units3():
	place = 3
	bound = [100, 500, 1000]
	labels3, values3 = [], []
	for i in range(3):
		primes = pg.get_prime_numbers(bound[i])
		labels, values = pd.get_digits(primes, place)
		labels3 += [labels]
		values3 += [values]

		dp.plot_primes(primes, bound[i])
		dp.plot_consol(labels, values, 'Digit')
	
	dp.plot_3digit_curve(labels3, values3)


main()