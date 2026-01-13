import pymssql
import dbconfig_new
import pyodbc

#한글 처리 문제로 pymssql 은 컬럼명이 필요한경우에만 ex) 마진계산 DB
#defalut 는 pyodbc
class Database():

	def __init__(self,site,func=False):
		self.site = site
		self.func = func
		self.connetDB()

	def connetDB(self):
		#self.getDbAccount()
		dbinfo = dbconfig_new.DbAccount(self.site)
		#self.site_account = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(dbinfo['host'], dbinfo['db'], dbinfo['user'], dbinfo['password'])

		if self.func == False:
			#self.db = pymssql.connect(server=dbinfo['host'], user=dbinfo['user'], password=dbinfo['password'], database=dbinfo['db'], autocommit=True)
			self.site_account = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(dbinfo['host'], dbinfo['db'], dbinfo['user'], dbinfo['password'])
			self.db = pyodbc.connect(self.site_account, autocommit=True)
		else:
			#self.db = pymssql.connect(self.site_account, autocommit=True, as_dict=True)
			host_db = dbinfo['host']
			self.db = pymssql.connect(server=host_db.replace(',',':'), user=dbinfo['user'], password=dbinfo['password'], database=dbinfo['db'], autocommit=True, as_dict=True)

		self.cursor = self.db.cursor()

	def close(self):
		self.db.close()

	def commit(self):
		self.db.commit()

	def selectone(self,query):
		self.cursor.execute(query)
		self.row = self.cursor.fetchone()
		return self.row

	def select(self,query):
		self.cursor.execute(query)
		self.row = self.cursor.fetchall()
		return self.row

	def execute(self,query):
		self.cursor.execute(query)

	def insert(self,table,dic):
		sql = "INSERT INTO {0} ".format(table)
		column_sql = ""
		value_sql = ""
		dic_low = 1
		for key, values in dic.items():
			column_sql = column_sql + str(key)
			value_sql = value_sql + str(values)
			if dic_low < len(dic):
				column_sql = column_sql + ", "
				value_sql = value_sql + ", "
			dic_low += 1
		sql = sql + "(" + column_sql + ") VALUES (" + value_sql + ")"

		self.cursor.execute(sql)

	def update(self,table,dic,where):
		sql = "UPDATE {0} SET ".format(table)
		set_sql = ""
		dic_low = 1
		for key, values in dic.items():
			set_sql = set_sql + str(key) + "=" + str(values)
			if dic_low < len(dic):
				set_sql = set_sql + ", "
			dic_low += 1
		sql = sql + set_sql + " WHERE {0}".format(where)
		self.cursor.execute(sql)

	def delete(self,table,where):
		sql = "DELETE FROM {0}".format(table)
		if where != None or where != '' :
			sql = sql + " where {0}".format(where)
		self.cursor.execute(sql)