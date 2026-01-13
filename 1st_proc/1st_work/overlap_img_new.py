import os
import datetime
import sys
import hashlib
import csv
import socket
import time
import DBmodule_FR

global ver
ver = "1.03"
print(">> ver : {}".format(ver))
ins_cnt = 0
upd_cnt = 0
file_list = {}
overlap_list = {}
LIMITED_SIZE = 65536

local_ip = socket.gethostbyname(socket.getfqdn())
#path = "C:\\project\\chromedriver.exe"

db_FS = DBmodule_FR.Database('freeship')

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


def setProcLog(db_FS, siteName, i_cnt, u_cnt, fromDate, toDate, memoKbn, p_state):
    siteno = getProcSiteNo(siteName)
    #print("siteno :"+str(siteno))

    if i_cnt == 0 and u_cnt == 0:
        log_msg = "[ " + siteno + " ] " + str(siteName)
    else:
        log_msg = "[ " + siteno + " ] " + str(siteName) + " : " + str(i_cnt) + " : " + str(u_cnt)
    #print("setProcLog log_msg : "+str(log_msg))

    sql_s = "select top 1 procDate from freeship_overlap_img_work where memo = '" + str(memoKbn) + "' and procDate = '" + str(toDate) + "' and site = '"+str(siteName)+"' "
    rowSel = db_FS.selectone(sql_s)
    if rowSel:
        if p_state == 'S':
            up_sql = "update freeship_overlap_img_work set state='"+str(p_state)+"', sDate = getdate(), log_msg = '" + str(log_msg) + "' where memo = '" + str(memoKbn) + "' and procDate = '" + str(toDate) + "' and site = '"+str(siteName)+"' "
        else:
            up_sql = "update freeship_overlap_img_work set state='"+str(p_state)+"', eDate = getdate(), log_msg = '" + str(log_msg) + "' where memo = '" + str(memoKbn) + "' and procDate = '" + str(toDate) + "' and site = '"+str(siteName)+"' "

        #print("update freeship_overlap_img_work : "+str(up_sql))
        db_FS.execute(up_sql)
    else:
        up_sql = "insert into freeship_overlap_img_work (procDate, state, sDate, memo, site, targetSdate, targetEdate) values ('"+str(
            toDate)+"','"+str(p_state)+"',getdate(),'" + str(memoKbn) + "','" + str(siteName) + "','"+str(fromDate)+"','"+str(toDate)+"') "
        #print("insert freeship_overlap_img_work : "+str(up_sql))
        db_FS.execute(up_sql)

    return "0"


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
    elif ip == "59.23.231.196":
        return_array = ['baby', 'office', 'industry']
    elif ip == "211.195.9.71":
        return_array = ['mini']
    elif ip == "59.23.231.200":
        return_array = ['red']
    elif ip == "222.104.189.18":
        return_array = ['red']
    else:
        print(" Unmatch !!")
        return "1"

    return return_array


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

if __name__ == '__main__':

	now = datetime.datetime.now()
	print('>> 중복 이미지 작업 시작 :' + str(now))
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

	lastProcDate = ""
	toDay = datetime.datetime.today()
	toDay = str(toDay)
	toDay = toDay[:10]

	sql_day = "select top 1 eDate from freeship_overlap_img_work where memo = 'DB_update' and state='F' order by procDate desc"
	rowSel = db_FS.selectone(sql_day)
	if rowSel:
		lastProcDate = rowSel[0]
		# print(" LastProcDate : "+str(lastProcDate))
	# print(" >>" + str(lastProcDate)+" ~ "+str(toDay))

	#site = int(input(sitestr))
	site = int(sys.argv[1].strip()) # 사이트 입력
	#selectdate = input(datestr)
	#selectdate2 = input("날짜를 입력해주세요 끝날짜")

	savepath = "D:\jin"
	##### convert_date = datetime.datetime.strftime(datetime.datetime.strptime(selectdate, "%Y%m%d"), "%Y-%m-%d")
	convert_date = datetime.datetime.strftime(datetime.datetime.strptime(lastProcDate, "%Y-%m-%d"), "%Y-%m-%d")  # 변경 (24-05-03)
	end_date = datetime.datetime.now().strftime("%Y-%m-%d")
	#end_date = datetime.datetime.strftime(datetime.datetime.strptime(selectdate2, "%Y%m%d"), "%Y-%m-%d")

	sitedir = sitedic[site]
	print("==================================================")
	print(">> 사이트 번호 : {} [{}] ".format(site, sitedir))
	print(">> 날짜 : {} ~ {}".format(convert_date, end_date))
	print("==================================================")

	from_date = convert_date # 이미지 중복 기간 from
	to_date = end_date       # 이미지 중복 기간 to

	########### drive_path SET ############
	drive_path = "D"
	if local_ip == "59.23.231.195":
		drive_path = "E"
	elif local_ip == "211.195.9.73":
		if sitedir == "furniture":
			drive_path = "J" # 24.06.24 furniture 디렉토리 변경
		else:
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

	# site DB Open
	db_con = DBmodule_FR.Database(sitedir)

	sqlDel = "delete from a_TEMP_IMG "
	print(" delete a_TEMP_IMG ")
	db_con.execute(sqlDel)
	time.sleep(1)

	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 중복이미지 Read시작 :' + str(now))
	setProcLog(db_FS, sitedir, 0, 0, from_date, to_date, 'img_csv_read', 'S')
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

	setProcLog(db_FS, sitedir, ins_cnt, upd_cnt, from_date, to_date, 'img_csv_read', 'F')
	print(" setProcLog img_csv_save (F) ")
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 중복이미지 Read완료 :' + str(now))



	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 중복이미지 삭제시작 :' + str(now))
	setProcLog(db_FS, sitedir, 0, 0, from_date, to_date, 'img_csv_proc', 'S')
	time.sleep(2)
	print('time.sleep(2)')
	del_cnt = 0

	work_chk = ""
	sql = "select top 1 group_no from a_TEMP_IMG where sitecate = '{}'".format(sitedir)
	row_main = db_con.selectone(sql)
	if not row_main:
		print(">> No data ")
		work_chk = "0"
	else:
		work_chk = "1"
		group_no = row_main[0]

		sql2 = "select ali_no from a_TEMP_IMG where sitecate = '{}' and group_no = '{}'".format(sitedir, group_no)
		rows = db_con.select(sql2)
		if rows:
			all_tmp_ali_no = ""
			for row in rows:
				ali_no = row[0]
				if all_tmp_ali_no == "":
					all_tmp_ali_no = "'" + str(ali_no) + "'"
				else:
					all_tmp_ali_no = all_tmp_ali_no + "," + "'" + str(ali_no) + "'"

			sql3 = "select uid,isnull(naver_in,0),goodscode,ali_no,price, isnull(order_ck,'') from t_goods where IsDisplay = 'T' and ali_no in ("+str(all_tmp_ali_no)+") order by price asc"
			rows_goods = db_con.select(sql3)
			row_cnt = 0
			if rows_goods:
				for row_goods in rows_goods:
					guid = row_goods[0]
					naver_in = row_goods[1]
					goodscode = row_goods[2]
					ea_ali_no = row_goods[3]
					price = row_goods[4]
					order_ck = row_goods[5]

					if row_cnt == 0:
						print(">> [low price] ({}) [{}] goodscode: {} naver_in : {} | price : {} | order_ck : {}".format(row_cnt, ea_ali_no, goodscode, naver_in, price, order_ck))
					else:
						print(">> [loverlap] ({}) [{}] goodscode: {} naver_in : {} | price : {} | order_ck : {}".format(row_cnt, ea_ali_no, goodscode, naver_in, price, order_ck))
						if str(naver_in) == "1":
							sql4 = "select goodscode from naver_del where goodscode = '{}'".format(goodscode)
							row_chk = db_con.selectone(sql4)
							if not row_chk:
								sql_ins = "insert into naver_del (goodscode) values('{}')".format(goodscode)
								print(">> sql_ins : {}".format(sql_ins))
								db_con.execute(sql_ins)

						sql_ups = "update t_goods set Del_Naver=1 where uid = '{}'".format(guid)
						print(">> sql_ups : {}".format(sql_ups))
						db_con.execute(sql_ups)
						del_cnt = del_cnt + 1

					row_cnt = row_cnt + 1

		sql_del = "delete from a_TEMP_IMG where sitecate = '{}' and group_no = '{}'".format(sitedir, group_no)
		print(">> sql_del : {}".format(sql_del))
		db_con.execute(sql_del)   

	setProcLog(db_FS, sitedir, del_cnt, 0, from_date, to_date, 'img_csv_proc', 'F')
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 중복이미지 삭제완료 :' + str(now))


	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DB confirm goods = null 시작 :' + str(now))
	setProcLog(db_FS, sitedir, 0, 0, from_date, to_date, 'DB_update', 'S')
	if work_chk != "":
		sql5 = "select count(*) as cnt from a_TEMP_IMG sitecate = '{}'".format(sitedir)
		print(">> sql5 : {}".format(sql5))
		temp_row = db_con.selectone(sql5)   
		if temp_row[0] == 0:
			############ DB confirm_goods = null처리
			sel_sql = " select count(*) as db_cnt from t_goods where RegDate < '" +str(to_date)+ "' and confirm_goods='1' "
			row_db_cnt = db_con.selectone(sel_sql)
			confirm_cnt = row_db_cnt[0]
			if confirm_cnt > 0:
				db_up_sql = " update t_goods set confirm_goods=null where RegDate < '" +str(to_date)+ "' and confirm_goods='1' "
				print(">> db_up_sql : {}".format(db_up_sql))
				db_con.execute(db_up_sql)

	setProcLog(db_FS, sitedir, confirm_cnt, 0, from_date, to_date, 'DB_update', 'F')
	print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DB confirm goods = null 완료 :' + str(now))

	now = datetime.datetime.now()
	print('>> 중복 이미지 작업 완료 :' + str(now))

	db_con.close()
	db_FS.close()
	time.sleep(10)
	os._exit(0)

















	db_con.close()
	db_FS.close()
	print(" End processing.")
	time.sleep(10)
	sys.exit(0)
