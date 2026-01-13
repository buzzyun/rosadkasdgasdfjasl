import datetime, socket
import sharkda_category 
import DBmodule_FR

def getparse(target, findstr, laststr):
    result = ""
    if findstr:
        pos = target.find(findstr)
        if pos > -1:
            result = target[pos + len(findstr):]
    else:
        result = target
    if laststr:
        lastpos = result.find(laststr)
        if lastpos > -1:
            result = result[:lastpos]
    else:
        result = result
    return result.strip()

#rfind 파싱함수
def getparseR(target, findstr, laststr):
    if findstr:
        pos = target.rfind(findstr)
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

    print(str(datetime.datetime.now()))
    timecount = 0

    currIp = socket.gethostbyname(socket.gethostname())
    db_con = DBmodule_FR.Database('taobao')
    cnt_all = 0
    category_tmp = sharkda_category.category_source
    category_all = getparse(category_tmp,'<li class="code','')
    cate_sp = category_all.split('<li class="code')
    cnt1 = 0
    for ea_cate in cate_sp:
        print("\n\n>> ---------------------------------------------")
        depth_code_1 = getparse(ea_cate,'-','">')
        depth_name_1 = getparse(ea_cate,'class="cate-name">','</span>')
        depth_source_1 = getparse(ea_cate,'<ul class="depth2">','')
        cnt1 = cnt1 + 1
        ## print(">> ({}) depth 1 [{}] {}".format(cnt1, depth_code_1, depth_name_1))

        cate_sp2 = depth_source_1.split('</ul>')
        cnt2 = 0
        for ea_cate2 in cate_sp2:
            depth_tmp_2 = getparse(ea_cate2,'','<div class="depth3-')
            depth_tmp_2 = getparse(depth_tmp_2,'<a href="','</a>')
            depth_code_2 = getparse(depth_tmp_2,'categoryNo/','">')
            depth_name_2 = getparse(depth_tmp_2,'">','')
            depth_source_2 = getparse(ea_cate2,'<ul class="depth3">','')
            if depth_code_2 != "":
                cnt2 = cnt2 + 1
                ## print(">> >> ({}) depth 2 [{}] {}".format(cnt2, depth_code_2, depth_name_2))

            cate_sp3 = depth_source_2.split('</li>')
            cnt3 = 0
            for ea_cate3 in cate_sp3:
                depth_tmp_3 = getparse(ea_cate3,'<a href="','</a>')
                depth_code_3 = getparse(depth_tmp_3,'categoryNo/','">')
                depth_name_3 = getparse(depth_tmp_3,'">','')
                if depth_code_3 != "":
                    cnt3 = cnt3 + 1
                    cnt_all = cnt_all + 1
                    print(">>({}) [{}] {} >> [{}] {} >> [{}] {} ".format(cnt_all, depth_code_1, depth_name_1, depth_code_2, depth_name_2, depth_code_3, depth_name_3))

                    sql = "select top 1 catecode from t_category_sharkda where catecode = '{}'".format(depth_code_3)
                    row = db_con.select(sql)
                    if row:
                        print(">> 존재하는 카테코드 : {}".format(depth_code_3))
                    else:
                        sql_i = "insert into t_category_sharkda (CateCode, Name, kor_name, depth, sort, parent, bcate, mcate, ishidden, big, middle, lastcate, up_date, list_in, update_cnt) values ({},'{}','{}',{},{},{},{},{},'{}','{}','{}',{}, getdate(),0,0)".format(depth_code_3, depth_name_3, depth_name_3, 3, cnt3, depth_code_2, depth_code_1, depth_code_2, 'F', depth_name_1,  depth_name_2, 1)
                        print(">> sql_i : {}".format(sql_i))
                        db_con.execute(sql_i)

    db_con.close()