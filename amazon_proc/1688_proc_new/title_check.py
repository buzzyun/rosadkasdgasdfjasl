
# -*- coding: utf-8 -*-
import datetime
import os
import random
import re
import json
import DBmodule_FR

#중국어 찾기
def findChinese(target):
    flag = False
    for n in re.findall(r'[\u4e00-\u9fff]+', target):
        flag = True
        break
    return flag

if __name__ == '__main__':

    print(">> Start ")
    print(str(datetime.datetime.now()))

    db_con = DBmodule_FR.Database("red")

    sql = "select uid, title, goodscode from t_goods "
    rows = db_con.select(sql)

    for row in rows:
        guid = row[0]
        title = row[1]
        goodscode = row[2]

        chk_Chinese = findChinese(title)
        if chk_Chinese == True:
            print(">> Find Chinese : {}".format(title))
            print(">> goodscode : {} (uid: {}) ".format(goodscode, guid))
            usql = "update t_goods set title_chk = confirm_goods, confirm_goods = '5' where uid = '{}'".format(guid)
            print(">> usql : {}".format(usql))
            db_con.execute(usql)
        else:
            print(">> No Chinese : {}".format(title))

    db_con.close()

    print(str(datetime.datetime.now()))
    print(" end ")