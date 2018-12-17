#
#   DBclass based on SQLite specific for csound server and clients
#	15-09-2018:	made it 3.5 compatible
#
import csv, os, random, sqlite3, sys, time, datetime

from functools import partial

showinserts = 0
showupdates = 0
showselects = 0

class db(object):
	def __init__( self, dbname = './csounds.sqlite' ):
		self.DBFILE = dbname
		self.conn = sqlite3.connect( self.DBFILE, detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread = False )
		self.conn.row_factory = sqlite3.Row     # allows query results as dictionaries
		self.cur = self.conn.cursor()

	def insert(self, insq, tup):
		if showinserts:print(insq, tup)
		try:
			self.cur.execute(insq, tup)
			self.conn.commit()
			#print self.cur.rowcount
		except sqlite3.Error as e:
			print("Error {}:".format(e.args[0]))

	def update(self, upq):
		if showupdates:print(upq)
		try:
			self.cur.execute(upq)
			self.conn.commit()
			#print self.cur.rowcount
		except sqlite3.Error as e:
			print("Error %s:" % e.args[0])


	def select(self, selq):
		if showselects: print(selq)
		self.cur.execute(selq)
		rows = self.cur.fetchall()
		return rows

	def exists(self, selq):     # returns true or false depending on query
		self.cur.execute(selq)
		rows = self.cur.fetchall()
		if len(rows) == 0:
			result = False
		else:
			result = True
		return result


if __name__ == '__main__':
	csdb = db()
	instr = csdb.select("select name, gui, procgui from instruments where name ='FM bass 1'")
	#for ins in instr:
	print(instr[0]['name'], instr[0]['gui'])