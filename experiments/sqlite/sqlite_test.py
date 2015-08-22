#!/usr/bin/python

import sqlite3
import os
import sys

def to_be_excluded(path):
	return False

DB_FILE = ":memory:"
#DB_FILE = "sample.db"

repo_map = sqlite3.connect(DB_FILE)
repo_cursor = repo_map.cursor()

repo_cursor.execute('''CREATE TABLE IF NOT EXISTS files (remote_id text, is_file boolean, path text, size int, local_mtime integer, remote_mtime text)''')

repo_cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (local_path text, remote_path text, is_done boolean, created_time integer)''')

repo_map.commit()

"""
# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
"""

ROOT_PATH = os.path.expanduser("~/OneDrive")
for root, dirs, files in os.walk(ROOT_PATH):
	values = []
	values.append(("Unknown", 0, root, 0, 0, "YYYY-mm-dd hh:mm:ss"))
	#print "root " + "*" * 20
	#print root
	# insecure!!!
	# repo_cursor.execute("INSERT INTO files VALUES (0, 0, '" + root + "', 0, 0)")
	#print "*" * 20
	#print dirs
	#print "*" * 20
	#print files
	
	for item in files:
		file_path = os.path.join(root, item)
		mode = os.stat(file_path)
		values.append(("Unknown", 1, file_path, mode.st_size, mode.st_mtime, "YYYY-mm-dd hh:mm:ss"))
	
	repo_cursor.executemany("INSERT INTO files VALUES (?, ?, ?, ?, ?, ?)", values)
		# insecure!!
		#repo_cursor.execute("INSERT INTO files VALUES (0, 1, '" + file_path + "', " + str(mode.st_size) + ", " + str(mode.st_mtime) + ")")
	
	repo_map.commit()

rows = repo_cursor.execute("SELECT * from files")

for row in rows:
   print "REMOTE_ID=", str(row[0]), ", IS_FILE=", str(row[1]), ", PATH=", str(row[2]), ", SIZE=", str(row[3]), ", MTIME=", str(row[4]), "\n"

#import signal
#signal.pause()

repo_map.close()
