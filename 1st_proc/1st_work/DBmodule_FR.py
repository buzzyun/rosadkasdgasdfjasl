import pyodbc


class Database():

    def __init__(self, site):
        self.site = site
        self.connetDB()

    def getDbAccount(self):
        print("DB SEL : "+str(self.site))
        if self.site.lower() == 'taobao':
            SERVER = '211.195.9.69,14103'
            DATABASE = 'cn'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'cn':
            SERVER = '211.195.9.69,14103'
            DATABASE = 'cn'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'naver_ep':
            SERVER = '211.195.9.68,14103'
            DATABASE = 'ep'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'naver_ep2':
            SERVER = '211.195.9.68,14103'
            DATABASE = 'ep2'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'naver_price':
            SERVER = '211.195.9.71,14103'
            DATABASE = 'naver_price'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'mini':
            SERVER = '211.195.9.71,14103'
            DATABASE = 'mini'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        
        elif self.site.lower() == 'shop':
            SERVER = '211.195.9.69,14103'
            DATABASE = 'shop'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'trend':
            SERVER = '211.195.9.70,14103'
            DATABASE = 'trend'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'ref':
            SERVER = '211.195.9.69,14103'
            DATABASE = 'REF'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'freeship':
            SERVER = '59.23.231.194,14103'
            DATABASE = 'freeship'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'aliexpress':
            SERVER = '59.23.231.194,14103'
            DATABASE = 'aliexpress'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'best':
            SERVER = '59.23.231.197,14103'
            DATABASE = 'BEST'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'global':
            SERVER = '59.23.231.197,14103'
            DATABASE = 'global'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'usa':
            SERVER = '59.23.231.206,14103'
            DATABASE = 'USA'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011#206'
        elif self.site.lower() == 'mall':
            SERVER = '59.23.231.206,14103'
            DATABASE = 'MALL'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011#206'
        elif self.site.lower() == 'de':
            SERVER = '59.23.231.202,14103'
            DATABASE = 'DE'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'uk':
            SERVER = '59.23.231.202,14103'
            DATABASE = 'UK'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'handmade':
            SERVER = '59.23.231.202,14103'
            DATABASE = 'handmade2'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'fashion':
            SERVER = '59.23.231.195,14103'
            DATABASE = 'fashion'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'electron':
            SERVER = '59.23.231.195,14103'
            DATABASE = 'electron'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'furniture':
            SERVER = '211.195.9.73,14103'
            DATABASE = 'furniture'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'beauty':
            SERVER = '211.195.9.73,14103'
            DATABASE = 'beauty'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'jewelry':
            SERVER = '211.195.9.73,14103'
            DATABASE = 'jewelry'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'auto':
            SERVER = '211.195.9.74,14103'
            DATABASE = 'auto'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'sports':
            SERVER = '211.195.9.74,14103'
            DATABASE = 'sports'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'baby':
            SERVER = '59.23.231.196,14103'
            DATABASE = 'baby'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'office':
            SERVER = '59.23.231.196,14103'
            DATABASE = 'office'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'industry':
            SERVER = '59.23.231.196,14103'
            DATABASE = 'industry'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'fashion2':
            SERVER = '59.23.231.198,14103'
            DATABASE = 'fashion2'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'electron2':
            SERVER = '59.23.231.198,14103'
            DATABASE = 'electron2'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'furniture2':
            SERVER = '211.195.9.66,14103'
            DATABASE = 'furniture3'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'beauty2':
            SERVER = '211.195.9.66,14103'
            DATABASE = 'beauty5'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'jewelry2':
            SERVER = '211.195.9.66,14103'
            DATABASE = 'jewelry2'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'auto2':
            SERVER = '59.23.231.199,14103'
            DATABASE = 'auto3'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'sports2':
            SERVER = '59.23.231.199,14103'
            DATABASE = 'sports3'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'baby2':
            SERVER = '211.195.9.67,14103'
            DATABASE = 'baby3'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'office2':
            SERVER = '211.195.9.67,14103'
            DATABASE = 'office3'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'industry2':
            SERVER = '211.195.9.67,14103'
            DATABASE = 'industry3'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@allin#am1071'
        elif self.site.lower() == 'red':
            SERVER = '211.195.9.71,14103' # 23.03.16 변경 59.23.231.200 --> 211.195.9.72
            DATABASE = 'temu'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'
        elif self.site.lower() == 'navernoclick':
            SERVER = '211.195.9.69,14103'
            DATABASE = 'navernoclick'
            USERNAME = '1stplatfor_sql'
            PASSWORD = '@admin#db1011'

        self.site_account = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3}'.format(
            SERVER, DATABASE, USERNAME, PASSWORD)

    def connetDB(self):
        self.getDbAccount()
        self.db = pyodbc.connect(self.site_account, autocommit=True)
        self.cursor = self.db.cursor()
        # print('[connetDB()]')

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

    def executeRep(self, sql):
        sql = sql.replace("\\'","'")
        sql = sql.replace("None","0")
        #print("[insert] sql : " + str(sql))
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
