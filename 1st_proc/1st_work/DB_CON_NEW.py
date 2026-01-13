import pyodbc
from dotenv import load_dotenv
import os

# 하위 폴더의 .env 파일 경로
# dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')

# 현재 디렉토리의 .env 파일 로드
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

class Database():

    def __init__(self, site):
        self.site = site
        self.connetDB()

    def getDbAccount(self):
        print("DB SEL : "+str(self.site))

        # 데이터베이스 연결 설정
        SERVER = os.getenv('SERVER_'+self.site.upper())
        DATABASE = os.getenv('DATABASE_'+self.site.upper())
        USERNAME = os.getenv('USERNAME_'+self.site.upper())
        PASSWORD = os.getenv('PASSWORD_'+self.site.upper())

        self.site_account = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(
            SERVER, DATABASE, USERNAME, PASSWORD)
        #print(">> site_account : " + self.site_account)

    def connetDB(self):
        self.getDbAccount()
        self.db = pyodbc.connect(self.site_account, autocommit=True)
        self.cursor = self.db.cursor()
        #print('[connetDB()]')

    def close(self):
        self.db.close()
        # print('[db.close()]')

    def selectone(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        #print('[selectone] sql : ' +str(query))
        return row

    def select(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        #print('[select] sql : ' +str(query))
        return row

    def insert(self, table, dic):
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
        #print("[insert] sql : " + str(sql))
        self.cursor.execute(sql)

    def execute(self, sql):
        self.cursor.execute(sql)

    def update(self, table, dic, where):
        sql = "UPDATE {0} SET ".format(table)
        set_sql = ""
        dic_low = 1
        for key, values in dic.items():
            set_sql = set_sql + str(key) + "=" + str(values)
            if dic_low < len(dic):
                set_sql = set_sql + ", "
            dic_low += 1
        sql = sql + set_sql + " WHERE {0}".format(where)
        #print("[update] sql : " + str(sql))
        self.cursor.execute(sql)

    def delete(self, table, where):
        sql = "DELETE FROM {0}".format(table)
        if where != None or where != '':
            sql = sql + " where {0}".format(where)
        #print("[delete] sql : " + str(sql))
        self.cursor.execute(sql)
