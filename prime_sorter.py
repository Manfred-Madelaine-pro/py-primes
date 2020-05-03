

def sort_primes(primes, group):
	prime_groups = group_by(primes, group)
	return get_len(prime_groups)


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

