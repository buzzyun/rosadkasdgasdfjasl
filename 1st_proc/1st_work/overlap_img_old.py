import glob
import os
import datetime
import sys
import hashlib
import csv
import socket
import time
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
import DBmodule_FR

ins_cnt = 0
upd_cnt = 0
file_list = {}
overlap_list = {}
LIMITED_SIZE = 65536

local_ip = socket.gethostbyname(socket.getfqdn())
#path = "C:\\project\\chromedriver.exe"


def getProcSiteNo(sitedir):

    siteNo = ""
    if sitedir == "red":
        siteNo = "11"
    elif sitedir == "fashion2":
        siteNo = "1"
    elif sitedir == "electron2":
        siteNo = "2"
    elif sitedir == "furniture2":
        siteNo = "3"
    elif sitedir == "beauty2":
        siteNo = "4"
    elif sitedir == "jewelry2":
        siteNo = "5"
    elif sitedir == "auto2":
        siteNo = "6"
    elif sitedir == "sports2":
        siteNo = "7"
    elif sitedir == "baby2":
        siteNo = "8"
    elif sitedir == "office2":
        siteNo = "9"
    elif sitedir == "industry2":
        siteNo = "10"
    elif sitedir == "fashion":
        siteNo = "12"
    elif sitedir == "electron":
        siteNo = "13"
    elif sitedir == "furniture":
        siteNo = "14"
    elif sitedir == "beauty":
        siteNo = "15"
    elif sitedir == "jewelry":
        siteNo = "16"
    elif sitedir == "auto":
        siteNo = "17"
    elif sitedir == "sports":
        siteNo = "18"
    elif sitedir == "baby":
        siteNo = "19"
    elif sitedir == "office":
        siteNo = "20"
    elif sitedir == "industry":
        siteNo = "21"
    elif sitedir == "mini":
        siteNo = "22"
    return siteNo


def setProcLog(db_FS, siteName, i_cnt, u_cnt, pDate, nDate, memoKbn, p_state):
    siteno = getProcSiteNo(siteName)
    #print("siteno :"+str(siteno))

    if i_cnt == 0 and u_cnt == 0:
        log_msg = "[ " + siteno + " ] " + str(siteName)
    else:
        log_msg = "[ " + siteno + " ] " + str(siteName) + " : " + str(i_cnt) + " : " + str(u_cnt)
    #print("setProcLog log_msg : "+str(log_msg))

    sql_s = "select top 1 procDate from freeship_overlap_img_work where memo = '" + str(memoKbn) + "' and procDate = '" + str(nDate) + "' and site = '"+str(siteName)+"' "
    rowSel = db_FS.selectone(sql_s)
    if rowSel:
        if p_state == 'S':
            up_sql = "update freeship_overlap_img_work set state='"+str(p_state)+"', sDate = getdate(), log_msg = '" + str(log_msg) + "' where memo = '" + str(memoKbn) + "' and procDate = '" + str(nDate) + "' and site = '"+str(siteName)+"' "
        else:
            up_sql = "update freeship_overlap_img_work set state='"+str(p_state)+"', eDate = getdate(), log_msg = '" + str(log_msg) + "' where memo = '" + str(memoKbn) + "' and procDate = '" + str(nDate) + "' and site = '"+str(siteName)+"' "

        #print("update freeship_overlap_img_work : "+str(up_sql))
        db_FS.execute(up_sql)
    else:
        up_sql = "insert into freeship_overlap_img_work (procDate, state, sDate, memo, site, targetSdate, targetEdate) values ('"+str(
            nDate)+"','"+str(p_state)+"',getdate(),'" + str(memoKbn) + "','" + str(siteName) + "','"+str(pDate)+"','"+str(nDate)+"') "
        #print("insert freeship_overlap_img_work : "+str(up_sql))
        db_FS.execute(up_sql)

    return "0"


def setProcDB(db_SiteCon,pDate,nDate):
    
	goodsCnt = 0
	goodsCnt2 = 0

	sql_s = " select count(*) as cnt from t_goods where RegDate >= '"+str(pDate)+"' and RegDate < '"+str(nDate)+"' and confirm_goods='1' "
	#print("sql_s : "+str(sql_s))
	rowSel = db_SiteCon.selectone(sql_s) 
	if rowSel:
		goodsCnt = rowSel[0]
		#print(" T_goods (confirm_goods) before : "+str(goodsCnt))

	up_sql = " UPDATE t_goods SET confirm_goods=null where RegDate >= '"+str(pDate)+"' and RegDate < '"+str(nDate)+"' "
	#print("up_sql : "+str(up_sql))
	db_SiteCon.execute(up_sql)

	time.sleep(1)

	sql_s = " select count(*) as cnt from t_goods where RegDate >= '"+str(pDate)+"' and RegDate < '"+str(nDate)+"' and confirm_goods='1' "
	#print("sql_s : "+str(sql_s))
	rowSel = db_SiteCon.selectone(sql_s) 
	if rowSel:
		goodsCnt2 = rowSel[0]
		#print(" T_goods (confirm_goods) after : "+str(goodsCnt2))

	time.sleep(1)

	return goodsCnt


def getSite(ip):

    return_array = ""
    if ip == "59.23.231.198":
        return_array = ['fashion2', 'electron2']
    elif ip == "59.23.231.199":
        return_array = ['auto2', 'sports2']
    elif ip == "211.195.9.66":
        return_array = ['beauty2', 'furniture2', 'jewelry2']
    elif ip == "211.195.9.67":
        return_array = ['baby2', 'office2', 'industry2']
    elif ip == "59.23.231.200":
        return_array = ['red']
    elif ip == "211.195.9.73":
        return_array = ['furniture', 'jewelry', 'beauty']
    elif ip == "59.23.231.195":
        return_array = ['fashion', 'electron']
    elif ip == "211.195.9.74":
        return_array = ['auto', 'sports']
    elif ip == "211.195.9.71":
        return_array = ['mini']
    elif ip == "59.23.231.200":
        return_array = ['red']
    else:
        print(" Unmatch !!")
        return "1"

    return return_array


site_array = getSite(local_ip)
if site_array == "1":
    print(" Input Error ")
    os._exit(1)

sitestr_temp = ""
ea_low = 1
sitedic = dict()
for sitecate in site_array:
    sitestr_temp = sitestr_temp + "{0}".format(ea_low) + "." + sitecate + "\n"
    sitedic[ea_low] = sitecate
    ea_low = ea_low + 1

sitestr = """
============================
{0}
============================
사이트 번호를 입려해주세요.(ver=1.0):
""".format(sitestr_temp)

datestr = """
날짜를 입력해 주세요. (YYYYMMDD):
"""


def getHashValue(filepath):
    chunksize = LIMITED_SIZE
    hash = hashlib.md5()

    with open(filepath, 'rb') as afile:
        buf = afile.read(chunksize)
        while len(buf) > 0:
            buf = afile.read(chunksize)
            hash.update(buf)

    retHash = hash.hexdigest()
    # print retHash
    return retHash


def getMyHash(filepath):
    chunksize = 1024
    with open(filepath, 'rb') as afile:
        buf = afile.read(chunksize)

    buf = buf + '0.62700000000000000000000000000000000000000000000000000000000'.encode()
    return buf[0:1024]


def dofilecmp(f1, f2):
    bufsize = LIMITED_SIZE
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        b1 = fp1.read(bufsize)
        b2 = fp2.read(bufsize)
        if b1 != b2:
            return False
        return True


def dofilecmp2(f1, f2):
    bufsize = LIMITED_SIZE
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True


def getparse(target, findstr, laststr):
    if findstr:
        pos = target.find(findstr)
        result = target[pos+len(findstr):]
    else:
        result = target

    if laststr:
        lastpos = result.find(laststr)
        result = result[:lastpos]
    else:
        result = result

    return result


site = int(input(sitestr))
selectdate = input(datestr)
savepath = "D:\jin"
convert_date = datetime.datetime.strftime(datetime.datetime.strptime(selectdate, "%Y%m%d"), "%Y-%m-%d")
end_date = datetime.datetime.now().strftime("%Y-%m-%d")

sitedir = sitedic[site]

########### drive_path SET ############
drive_path = "D"
if local_ip == "59.23.231.195":
    drive_path = "E"
elif local_ip == "211.195.9.73":
    drive_path = "E"
elif local_ip == "211.195.9.74":
    drive_path = "E"
elif local_ip == "211.195.9.71":
    drive_path = "G"
########################################

sitepath = r"{0}:\{1}\GoodsImg".format(drive_path, sitedir)
lists = os.listdir(sitepath)

print(" Sitedir : "+str(sitedir))
print(" Sitepath : "+str(sitepath))
for category in lists:
    if category != 'desktop.ini':

        catepath = r"{0}:\{1}\GoodsImg\{2}".format(drive_path, sitedir, category)
        imglists = os.listdir(catepath)

        for datelist in imglists:
            ea_datelist = datelist.replace("-", "")
            #print(" ea_datelist : "+str(ea_datelist))
            if str(ea_datelist).isdigit() == False:
                #print(" No isdigit : "+str(ea_datelist))
                pass
            else:
                convert_datelist = datetime.datetime.strftime(datetime.datetime.strptime(ea_datelist, "%Y%m%d"), "%Y-%m-%d")
                #print(" convert_datelist : "+str(convert_datelist))

                if convert_datelist >= convert_date and convert_datelist < end_date:
                    imgpath = r"{0}:\{1}\GoodsImg\{2}\{3}".format(drive_path, sitedir, category, datelist)
                    for path, dir, files in os.walk(imgpath):
                        for filename in files:
                            tf = os.path.join(path, filename)
                            file_list[tf] = os.path.getsize(tf)
                            if overlap_list.get(file_list[tf]) == None:
                                overlap_list[file_list[tf]] = 1
                            else:
                                overlap_list[file_list[tf]] += 1

print(" Start find same size files")

bigdupfile = {}
smalldupfile = {}

for key, value in file_list.items():
    if overlap_list[value] != None and overlap_list[value] >= 2:
        if value < LIMITED_SIZE:
            if smalldupfile.get(value) != None:
                smalldupfile[value].append(key)
            else:
                smalldupfile[value] = [key]
        else:
            if bigdupfile.get(value) != None:
                bigdupfile[value].append(key)
            else:
                bigdupfile[value] = [key]

result = {}
print(" Start get same files")
filecount = 1
for key, aValue in smalldupfile.items():
    myHash = {}
    for f in aValue:
        fileHash = getMyHash(f)
        if myHash.get(fileHash) != None:
            myHash[fileHash].append(f)
        else:
            myHash[fileHash] = [f]

    tmpResult = list(filter(lambda x: len(x) >= 2, myHash.values()))
    value = []
    for files in tmpResult:
        value += files
    if len(value) > 0:
        removedFile = []
        while True:
            result[filecount] = []
            size = len(value)
            for f in range(1, size):
                if dofilecmp(value[0], value[f]) == True:
                    result[filecount].append(value[f])
                    removedFile.append(value[f])
            result[filecount].append(value[0])
            removedFile.append(value[0])
            value = list(set(value) - set(removedFile))
            filecount += 1
            if len(value) == 0:
                break

nextFileCount = filecount + 10
filecount = len(bigdupfile)
print(" filecount : "+str(filecount))

for key, value in bigdupfile.items():
    myHash = {}
    for f in value:
        fileHash = getMyHash(f)
        if myHash.get(fileHash) != None:
            myHash[fileHash].append(f)
        else:
            myHash[fileHash] = [f]

    tmpResult = list(filter(lambda x: len(x) >= 3, myHash.values()))
    aDupfile = []
    for files in tmpResult:
        aDupfile += files

    filecount = len(aDupfile)
    if filecount >= 1:
        for file in aDupfile:

            fileHash = getHashValue(file)
            if result.get(fileHash) != None:
                result[fileHash].append(file)
            else:
                result[fileHash] = [file]

    tmpOnlyTwoFiles = list(filter(lambda x: len(x) == 2, myHash.values()))
    filecount = len(tmpOnlyTwoFiles)

    if filecount >= 1:
        for files in tmpOnlyTwoFiles:
            result[nextFileCount] = []
            if dofilecmp2(files[0], files[1]):
                result[nextFileCount].append(files[0])
                result[nextFileCount].append(files[1])
                nextFileCount += 1

######################################################################
ins_cnt = 0
upd_cnt = 0
f_cnt = 0
in_log_msg = ""
lastProcDate = ""
toDay = datetime.datetime.today()
toDay = str(toDay)
toDay = toDay[:10]

db_FS = DBmodule_FR.Database('freeship')
sql_day = "select top 1 procdate from freeship_overlap_img_work where procdate <> '" + str(toDay) + "' and memo = 'img_csv_read' and state='F' order by procDate desc"
rowSel = db_FS.selectone(sql_day)
if rowSel:
    lastProcDate = rowSel[0]
    print(" LastProcDate : "+str(lastProcDate))

print(" >>" + str(lastProcDate)+" ~ "+str(toDay))
# site DB Open
db_con = DBmodule_FR.Database(sitedir)

# setProcLog(db_FS, sitedir, 0, 0, lastProcDate, toDay, 'DB_update', 'S')
# print(" setProcLog DB_update (S) ")
# time.sleep(1)

# # site DB confirm_goods = null
# rtnCnt = setProcDB(db_con, lastProcDate, toDay)
# print(" setProcDB : confirm_goods = null OK : " + str(rtnCnt))
# time.sleep(1)

# setProcLog(db_FS, sitedir, rtnCnt, 0, lastProcDate, toDay, 'DB_update', 'F')
# print(" setProcLog DB_update (F) ")
# time.sleep(1)

sqlDel = "delete from a_TEMP_IMG "
print(" delete a_TEMP_IMG ")
db_con.execute(sqlDel)
time.sleep(1)

setProcLog(db_FS, sitedir, 0, 0, lastProcDate, toDay, 'img_csv_read', 'S')
print(" setProcLog img_csv_save (S) ")
time.sleep(1)

######################################################################

if len(result) > 1:
    results = list(filter(lambda x: len(x) >= 2, result.values()))
    if len(results) >= 1:

        print(' Start save csv file')
        logfile = open(savepath+'\\'+sitedir+'_'+datetime.datetime.now().strftime(
            "%Y%m%d")+'.csv', 'w', encoding='utf-8', newline='')
        csvfile = csv.writer(logfile)
        group_no = 0

        for row in results:
            group_no += 1
            for arow in row:
                savelist = []
                savelist.append(sitedir)
                cate_idx = getparse(arow, 'GoodsImg\\', '\\')
                savelist.append(cate_idx)
                file_name = getparse(arow, 'Big\\', '.')
                file_name = str(file_name).strip()
                savelist.append('"'+file_name+'"')
                savelist.append(group_no)
                csvfile.writerow(savelist)
                f_cnt = f_cnt + 1
                #print(str(file_name) + " | " + str(cate_idx) + " | " + str(group_no))

                sql = "select top 1 ali_no from a_TEMP_IMG where ali_no = '" + str(file_name) + "' "
                rowS = db_con.selectone(sql)
                if not rowS:
                    sql_c = "insert into a_TEMP_IMG (sitecate,cate_idx,ali_no,group_no) values('"+str(
                        sitedir)+"','"+str(cate_idx)+"','"+str(file_name)+"','"+str(group_no)+"')"
                    #print("Insert table : "+str(file_name))
                    ins_cnt = ins_cnt + 1
                    db_con.execute(sql_c)
                else:
                    sql_c = "update a_TEMP_IMG set sitecate = '"+str(sitedir)+"', cate_idx = '"+str(
                        cate_idx)+"', group_no = '"+str(group_no)+"' where ali_no = '"+str(file_name)+"'"
                    #print("Update table: "+str(file_name))
                    upd_cnt = upd_cnt + 1
                    db_con.execute(sql_c)

        logfile.close()
        print(" Save csv OK")
        print(" FileCnt : {} | ins_cnt : {} | upd_cnt : {}".format(
            f_cnt, ins_cnt, upd_cnt))
    else:
        print(" No data (1). ")
else:
    print(" No data (2). ")

setProcLog(db_FS, sitedir, ins_cnt, upd_cnt, lastProcDate, toDay, 'img_csv_read', 'F')
print(" setProcLog img_csv_save (F) ")
db_con.close()
db_FS.close()
print(" End processing.")

aa = input("")
