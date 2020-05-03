import sqlite3

from prettytable import from_db_cursor



def get_connection(db_name):
	con = sqlite3.connect(db_name)
	con.row_factory = sqlite3.Row
	return con


def create_table(con):
	sql_create_primes_table = """
		CREATE TABLE IF NOT EXISTS primes (
		id integer PRIMARY KEY,
		primes integer UNIQUE,
		creation_date text NOT NULL); 
	"""
	with con:
		con.execute(sql_create_primes_table)

	rows = get_all_primes(con)


def insert_rows(con, rows):
	sql_insert_primes = """
		INSERT INTO primes(primes, creation_date) VALUES (?, DATETIME('now')
	);"""
	with con:
		try:
			con.executemany(sql_insert_primes, rows)
		except sqlite3.IntegrityError:
			return 'Line already exists.' 

	rows = get_all_primes(con)


def get_all_primes(con):
	sql_select_all_primes = """
		SELECT * FROM primes;
	"""
	return con.execute(sql_select_all_primes)
	

def print_table(rows):
	table = from_db_cursor(rows)
	print(table) 



# ----------------------- Test ---------------------------

def test_db_creation():
	con = get_connection(':memory:')
	create_table(con)

	rows = [
		(2,),
		(3,),
		(5,),
	]
	insert_rows(con, rows)
	rows = get_all_primes(con)
	print_table(rows)

	con.close()


# test_db_creation()