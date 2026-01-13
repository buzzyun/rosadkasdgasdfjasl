
import datetime
import os
import DBmodule_FR
import cate_tmp_new

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
    print(">> start ")
    errcnt = 0
    db_con = DBmodule_FR.Database('red')

    sql = "select catecode, name, cateurl, bcate, mcate from t_category where CateCode > 1000 and IsHidden = 'F' and lastcate = '1' and cate_keyword = '' " 
    rows = db_con.select(sql)
    for row in rows:
        catecode = row[0]
        name = row[1]
        cateurl = row[2]
        bcate = row[3]
        mcate = row[4]
        print(f">> [{catecode}] {name} | {bcate} | {mcate} | {cateurl}")
        print(">>")

        catetmp = getparse(str(cate_tmp_new.depth2_tmp),'<h2>'+str(bcate),'<h2>')
        if catetmp.find(cateurl) > -1:
            keyword = ""
            catename = getparse(str(catetmp),cateurl,'</a>')
            if catename.find('title="') > -1:
                keyword = getparse(str(catename),'title="','"')
            elif catename.find('alt="') > -1:
                keyword = getparse(str(catename),'alt="','"')
            elif catename.find('>') > -1:
                keyword = getparse(str(catename),'>','')
            else:
                keyword = catename
            print(">> catename : {}".format(catename))
            if keyword == "":
                print(">> keyword 없음 : {}".format(catetmp))
            else:
                print(">> keyword : {}".format(keyword))
                sql_u = f"update t_category set cate_keyword = N'{keyword}' where catecode = '{catecode}'"
                print(f">> sql_u : {sql_u}")
                db_con.execute(sql_u)
        else:
            print(">> catetmp 없음 : {}".format(catetmp))


    db_con.close()
    os._exit(0)
    #input(">> Key : ")

######
