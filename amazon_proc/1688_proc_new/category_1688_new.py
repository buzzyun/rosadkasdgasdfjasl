import datetime
import time
import os
import re
import DBmodule_FR
import cate_tmp
import cate_tmp_new

global errcnt 

db_con = DBmodule_FR.Database('red')

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

#db 특수단어 제거
def replaceQueryString(in_word) :
    result = in_word.replace("'","`").replace("&rdquo;"," ").replace('”',' ')
    result = result.replace("★","").replace("◆","").replace("/"," | ").replace(","," ").replace("&lt;","<").replace("&gt;",">")
    result = result.replace(r'\x26', ' ').replace('&amp;',' & ').replace('&AMP;',' & ').replace('&nbsp;',' ').replace('&NBSP;',' ')
    result = result.replace("&ndash;","-").replace("&times;"," x ")
    result = result.replace("&#39;","`").replace("&quot;","").replace("\\", "")
    result = result.replace("【","(").replace("】",")").replace("()","").replace("[]","").replace(";","")

    return result

def replace_str(str_tmp):
    str_tmp = str(str_tmp).replace('&amp;','&').replace(',','|').replace("&#39;", "`").replace("'", "`").replace("  ", " ").strip()
    return str_tmp

#reg 한글 체크
def regKrStrChk(in_str):
    result = ""

    chkStr = str(in_str).replace(' ','')
    chkStr = chkStr.strip()
    regStr = re.search('[가-힣]+',chkStr)

    if (regStr):
        result = "1"
    else:
        result = "0"

    return result

# Depth 1
def newCateDep1(browser):
    print('\n [--- newCateDep1 start ---] ')

    path_file = os.getcwd()
    result = ""
    result = '''
<ul class="ul-hangye clearfloat ariatheme" id="aria7fch79z0h4g">
    <li class="ariatheme"><a href="https://fuzhuang.1688.com?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariafcznxamwyyo" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">의류 시장</font></font></a></li>
    <li class="ariatheme" id="ariaphp8ydygf6o"><a href="https://fushi.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariajrf3d93fd1c" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">신발 가방 액세서리</font></font></a></li>
    <li class="ariatheme" id="ariae52q5kwq03s"><a href="https://sport.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="arialbxr4ul1cmo" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">야외 스포츠</font></font></a></li>
    <li class="ariatheme"><a href="https://muying.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariaft8jgtx7aoo" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">아동복 모자와 유아</font></font></a></li>
    <li class="ariatheme" id="ariaahmjo8vih74"><a href="https://enjoy.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariabfznc42dt0w" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">애완동물 공예</font></font></a></li>
    <li class="ariatheme"><a href="https://home.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="arianx6l6sgxl68" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">생활 필수품</font></font></a></li>
    <li class="ariatheme"><a href="https://auto.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariaj8t578luz74" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">자동차 액세서리</font></font></a></li>
    <li class="ariatheme" id="arial3rjk432oww"><a href="https://food.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="aria9boi39hir8g" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">식품 시장</font></font></a></li>
    <li class="ariatheme"><a href="https://jia.1688.com/" target="_blank" id="ariakjryuzk4gr4"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">홈 텍스타일 및 홈 데코레이션</font></font></a></li>
    <li class="ariatheme"><a href="https://mei.1688.com/" target="_blank"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">미용과 생활화학</font></font></a></li>
    <li class="ariatheme" id="arialt62rr1g5pc"><a href="https://3c.1688.com/" target="_blank" id="ariaaiewjqm1hu0"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">디지털 가전</font></font></a></li>
    <li class="ariatheme"><a href="https://dgdz.1688.com/" target="_blank" id="ariap8n4w8090ds"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">남서</font></font></a></li>
    <li class="ariatheme"><a href="https://af.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariapy1o3uynwxc" data-spm-anchor-id="a26304.12183230.0.0" class="ariafocus"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">보안</font></font></a></li>
    <li class="ariatheme"><a href="https://bz.1688.com/" target="_blank"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">포장 시장</font></font></a></li>
    <li class="ariatheme"><a href="https://ec.1688.com/" target="_blank" id="ariaoa6hmf3klvk"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">전자부품</font></font></a></li>
    <li class="ariatheme"><a href="https://jd.1688.com/" target="_blank" id="aria7jog0hile40"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">장비</font></font></a></li>
    <li class="ariatheme"><a href="https://fangzhi.1688.com/" target="_blank"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">섬유 시장</font></font></a></li>
    <li class="ariatheme"><a href="https://yqyb.1688.com/" target="_blank" id="ariaex1f7ki6a80"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">수단</font></font></a></li>
    <li class="ariatheme"><a href="https://plas.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariajnvhfjagykg" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">고무 시장</font></font></a></li>
    <li class="ariatheme"><a href="https://chem.1688.com/" target="_blank"><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">화학 원료</font></font></a></li>
    <li class="ariatheme"><a href="https://steel.1688.com/?spm=a26304.12183230.0.0.6691665bwSMdOw" target="_blank" id="ariafkv8o7zmjj4" data-spm-anchor-id="a26304.12183230.0.0" class=""><font class="ariatheme" style="vertical-align: inherit;"><font style="vertical-align: inherit;" class="ariatheme">강철</font></font></a></li>
</ul>
'''
    main_category = getparse(result,'<li','</ul>')
    sp_bcate = str(main_category).split('</li>')
    print(">> sp_bcate : {}".format(len(sp_bcate)-1))
    low1 = 0
    for ea_bcate in sp_bcate:
        ea_item = getparse(str(ea_bcate),'<a ','')
        bcate_url = getparse(str(ea_item),'href="','"')
        if bcate_url.find('?') > -1: bcate_url = getparse(str(bcate_url),'','?')
        bcate_name = getparse(str(ea_item),'class="ariatheme">','</font>')
        bcate_name = replace_str(bcate_name).strip()
        tran_bcate_name = bcate_name
        if bcate_url != "":
            print("\n\n------------------------------------------------------------------------------------------------------------")
            print(">> ( 1 Depth ) ({}) [{}] | {} | {} ".format(low1, bcate_name, tran_bcate_name, bcate_url))
            print("\n\n------------------------------------------------------------------------------------------------------------")

            sql = "select * from t_category where amz_cateurl = '{0}'".format(bcate_url)
            rs = db_con.selectone(sql)
            print('##select one## sql :' +str(sql))
            if not rs: # rs is None
                dic = dict()
                dic['name'] = "'" + bcate_name + "'"
                dic['kor_name'] = "'" + tran_bcate_name + "'"
                dic['depth'] = 1
                dic['sort'] = low1
                dic['big'] = "'" + tran_bcate_name + "'"

                print('New Category')
                dic['amz_cateurl'] = "'" + str(bcate_url) + "'"
                db_con.insert('t_category', dic)  # insert
                print('##insert## : t_category')
            else:
                print('>> Category 존재 : {}'.format(bcate_name))

        low1 = low1 + 1

    print('>> [--- newCateDep 1 End ---] ')
    return "0"

def newCateDep2(in_dep):
    print('\n [--- newCateDep2 start ---] ')

    sql = "select catecode, name, kor_name, amz_cateurl,parent,bcate,mcate,scate,dcate,big,middle,small,little,last,ecate,final,fcate,final1 from t_category where CateCode > 1000 and depth = '1' and ishidden='F' and lastcate is null "
    print('\n sql:' + str(sql))

    rows = db_con.select(sql)
    print('\n len(rows) :' + str(len(rows)))
    if not rows:
        print('\n ' + str(in_dep) + ' Depth 처리 완료 :' + str(len(rows)))
        return "F"

    cnt = 0
    low = 0
    while low < len(rows):
        cnt = cnt + 1
        bcate_catecode = rows[low][0]
        bcate_catename = rows[low][1]
        bcate_catekor_name = rows[low][2]
        bcate_cateurl = rows[low][3]
        print('\n -------------------------------------------------------------')
        print('\n [ ' + str(cnt) + ' ] ' + str(bcate_catecode) + ' | ' + str(bcate_catename) + ' | ' + str(bcate_catekor_name) )
        print('\n ' + str(bcate_cateurl))

        time.sleep(1)
        result = getparse(str(cate_tmp.depth2_tmp),'<h2>'+str(bcate_catecode),'<h2>')
        result_org = getparse(str(cate_tmp_new.depth2_tmp),'<h2>'+str(bcate_catecode),'<h2>')

        low_2 = 0
        if result.find('class="content ariatheme"') > -1:
            type = "1_content"
            category_tmp = getparse(str(result),'class="content ariatheme"','')
            category_tmp = getparse(str(category_tmp),'<ul ','')
            sp_cate = category_tmp.split('</li>')
        elif result.find('class="ch-menu-body') > -1:
            type = "2_menu"
            category_tmp = getparse(str(result),'class="ch-menu-item-title ariatheme','')
            category_tmp = getparse(str(category_tmp),'<ul ','')
            sp_cate = category_tmp.split('</li>')
        elif result.find('mod-category') > -1:
            type = "3_mode"
            category_tmp = getparse(str(result),'mod-category','')
            category_tmp = getparse(str(category_tmp),'</dt>','')
            sp_cate = category_tmp.split('</a>')
        else:
            type = "4_else"
            print(">> else : ")

        print('category_tmp : {}'.format(type))
        print(">> len(sp_cate) : {}".format(len(sp_cate)))

        mscate_cnt = 0
        print(">> sp_mcate ")
        print(">> ===================================================================================================== ")
        for ea_mcate in sp_cate:
            last_ck = '0'
            mcate_tmp = ea_mcate
            mcate_detail = getparse(str(result),mcate_tmp,'')
            while mcate_tmp.find('<font') > -1:
                rep_tmp = '<font ' + getparse(str(mcate_tmp),'<font','>') + '>'
                mcate_tmp = mcate_tmp.replace(rep_tmp, '')
            mcate_tmp = mcate_tmp.replace('<font >','').replace('<font>','').replace('</font>','').strip()

            if type == "1_content":
                mcate_tmp = getparse(str(mcate_tmp),'<a ','</a>')
                mcate_url = getparse(str(mcate_tmp),'href="','"')
            elif type == "2_menu":
                mcate_tmp = getparse(str(mcate_tmp),'<a ','</a>')
                mcate_url = getparse(str(mcate_tmp),'href="','"')
            elif type == "3_mode":
                mcate_tmp = getparse(str(mcate_tmp),'<a ','')
                mcate_url = getparse(str(mcate_tmp),'href="','"')
            else:
                print(f"Else 1 {mcate_tmp}")

            if mcate_tmp.find('title="') > -1:
                mcate_name = getparse(str(mcate_tmp),'title="','"')
            elif mcate_tmp.find('alt="') > -1:
                mcate_name = getparse(str(mcate_tmp),'alt="','"')
            elif mcate_tmp.find('>') > -1:
                mcate_name = getparse(str(mcate_tmp),'>','')
            else:
                print(f"Else 2 {mcate_tmp}")

            mcate_name = mcate_name.replace(', ',' & ')
            mcate_url_org = mcate_url
            name_org = ""

            if result_org.find(mcate_url_org) > -1:
                catename_tmp = getparse(str(result_org), mcate_url_org, '</a>')
                if catename_tmp.find('title="') > -1:
                    name_org = getparse(str(catename_tmp),'title="','"')
                elif catename_tmp.find('alt="') > -1:
                    name_org = getparse(str(catename_tmp),'alt="','"')
                elif catename_tmp.find('>') > -1:
                    name_org = getparse(str(catename_tmp),'>','')
                else:
                    if catename_tmp.find('</h2>') > -1:
                        catename_tmp = getparse(str(catename_tmp), '', '</h2>')                    
                    name_org = catename_tmp
                    if name_org.find('<') > -1:
                        name_org = getparse(str(name_org),'<','')
                #print(">> name_org : {}".format(name_org))
            else:


                print(f">> mcate_url_org 없음 ")
                
            mcate_url = mcate_url.replace('&amp;','&').strip()

            if mcate_url[:2] == "//":
                mcate_url = "https://" + mcate_url[2:]
            search_url = mcate_url
            if mcate_url.find('keywords=') > -1:
                keyword = getparse(str(mcate_url),'keywords=','&')
            elif mcate_url.find('adsSearchWord=') > -1:
                keyword = getparse(str(mcate_url),'adsSearchWord=','')
            else:
                keyword = ""
                if name_org.find('-------------------------') > -1:
                    search_url = ""
                    name_org = ""
                else:
                    search_url = getparse(str(mcate_url),'','1688.com') + '1688.com/selloffer/offer_search.html?keywords=' + str(name_org) + '.searchbox.input'
                print(f">> search_url : {search_url}")
            #print(">> keyword : {}".format(keyword))

            while mcate_tmp.find('<font') > -1:
                rep_tmp = '<font ' + getparse(str(mcate_tmp),'<font','>') + '>'
                mcate_tmp = mcate_tmp.replace(rep_tmp, '')
            mcate_tmp = mcate_tmp.replace('<font >','').replace('<font>','').replace('</font>','').strip()
            #print(f">> mcate_tmp : {mcate_tmp}")

            if mcate_name != "" and mcate_url != "":
                low_2 = low_2 + 1
                print(">> ( 2 Depth ) [{}] {} | {} | {} | {} ".format(low_2, mcate_name, keyword, name_org, mcate_url))
                print(">>>>>>>>>>>>>> {} >> {} ".format(bcate_catename, mcate_name))
                dic2 = dict()
                dic2['name'] = "'" + mcate_name + "'"
                dic2['kor_name'] = "'" + mcate_name + "'"
                dic2['depth'] = 2
                dic2['sort'] = low_2
                dic2['parent'] = bcate_catecode
                dic2['bcate'] = bcate_catecode
                dic2['big'] = "'" + bcate_catekor_name + "'"
                dic2['middle'] = "'" + mcate_name + "'"
                dic2['amz_cateurl'] = "'" + str(mcate_url) + "'"
                dic2['lastcate'] = "'1'"
                dic2['name_org'] = "N'" + name_org + "'"
                dic2['cateurl'] = "N'" + mcate_url_org + "'"
                dic2['search_url'] = "N'" + search_url + "'"
                dic2['cate_keyword'] = "'" + keyword + "'"

                print('New 2 Category : {}'.format(mcate_name))
                db_con.insert('t_category', dic2)  # insert
                print('##insert## : t_category')

                # sql2 = "select catecode, name, amz_cateurl from t_category where name_org = '{}' and amz_cateurl = '{}'".format(name_org, mcate_url)
                # #print('##select one## sql2 :' + str(sql2))
                # rs2 = db_con.selectone(sql2)
                # if not rs2: # rs2 is None
                #     print('New 2 Category : {}'.format(mcate_name))
                #     db_con.insert('t_category', dic2)  # insert
                #     print('##insert## : t_category')
                # else:
                #     print('mcate_name 존재 : {}'.format(mcate_name))
                #     cate2_catecode = rs2[0]
                #     cate2_name = rs2[1]
                #     cate2_amz_cateurl = rs2[2]
                #     # if cate2_amz_cateurl != "":
                #     #     sql_where = " catecode = '" + str(cate2_catecode) + "'"
                #     #     db_con.update('t_category', dic2, sql_where)  # update
                #     #     print('##update## : (cate2_amz_cateurl) t_category : ({}) {} | {}'.format(cate2_catecode, cate2_name, cate2_amz_cateurl))
                #     # continue
            else:
                print("\n>> ( 2 Depth ) xxxxxxxxxxxxxxxxx  [{}] {} | {} | {} | {} ".format(low_2, mcate_name, keyword, name_org, mcate_url))
                print(">>>>>>>>>>>>>> {} >> {} ".format(bcate_catename, mcate_name))
        low = low + 1

        sql_u = " update t_category set cate_kbn = '1' where catecode = '{}'".format(bcate_catecode)
        print('bcate ({}) proc end (sql_u) : {}'.format(bcate_catecode, sql_u))
        db_con.execute(sql_u)

    print('>> [--- newCateDep2 end ---] ')
    return "0"


if __name__ == '__main__':
    print(">> start ")
    errcnt = 0
    set_browser = "chrome"
    now_url = "https://www.1688.com/"

    # depth 2
    newCateDep2("1")

    db_con.close()
    os._exit(0)
    #input(">> Key : ")

######
