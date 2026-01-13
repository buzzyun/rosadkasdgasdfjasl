import datetime
import os
import time
import DBmodule_FR
import globas_source

global ver
ver = "241017"
print(">> var : {}".format(ver))
db_FS = DBmodule_FR.Database('freeship')

# 파싱함수
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

# 파싱함수 (뒤에서 부터 찾아서 파싱)
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

def procLogSet(in_proc_no, in_proc_state, in_proc_cnt, in_proc_memo):
    sql = " insert into auto_proc_log (proc_no, proc_state, proc_start, proc_end, proc_cnt, proc_memo) "
    if in_proc_state == "S":
        sql = sql + " values('" + str(in_proc_no) + "','S',getdate(),'','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    elif in_proc_state == "F":
        sql = sql + " values('" + str(in_proc_no) + "','F','',getdate(),'" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    else:
        sql = sql + " values('" + str(in_proc_no) + "','" + str(in_proc_state) + "','','','" + str(in_proc_cnt) + "','" + str(in_proc_memo) + "') "
    print(" setLogProc : " + str(sql))
    db_FS.execute(sql)


def get_string(tmp_str):
    if tmp_str.find('<font') > -1: tmp_str = getparse(tmp_str,"<font","</font>")
    if tmp_str.find('">') > -1: tmp_str = getparse(tmp_str,'">','')
    tmp_str = tmp_str.replace('&nbsp;','').strip()
    return tmp_str

if __name__ == '__main__':
    now = datetime.datetime.now()
    print("\n>>===========================================")
    print('>> globas hscode list save Start :' + str(now))

    result = globas_source.hscode_list
    result_tmp = getparse(result,'<tbody>','</tbody>')
    result_tmp = getparse(result_tmp,'비고 2','')
    sp_result = result_tmp.split('<td width="838" height="1" colspan="11" bgcolor="#cccccc"></td>')
    for ea_item in sp_result:
        print(">> ")
        if ea_item.find("hscode_click(") > -1:
            ea_hscode = get_string(getparse(ea_item,"hscode_click('","')")).strip()
            ea_name = get_string(getparse(ea_item,'<td width="245" height="30"',"</td>"))
            ea_eng_name = get_string(getparse(ea_item,'<td width="244" height="30"',"</td>"))
            ea_cate_name = get_string(getparse(ea_item,'<td width="80" height="30"','</td>'))
            ea_bigo1 = get_string(getparse(ea_item,'<td width="60" height="30"','</td>'))
            ea_bigo2 = get_string(getparse(ea_item,'<td width="140" height="30"','</td>'))

            print(">> [{}] {} | {} | {} | {} | {}".format(ea_hscode, ea_name, ea_eng_name, ea_cate_name, ea_bigo1, ea_bigo2))

            sql = "select globas_hscode from globas_hscode_list where globas_hscode = '{}'".format(ea_hscode)
            row = db_FS.selectone(sql)
            if not row:
                sql_i = "insert into globas_hscode_list (globas_hscode, globas_hsname, globas_eng_hsname, globas_catename, globas_bigo1, globas_bigo2 ) \
                    values ('{}','{}','{}','{}','{}','{}')".format(ea_hscode, ea_name, ea_eng_name, ea_cate_name, ea_bigo1, ea_bigo2)
                db_FS.execute(sql_i)

    time.sleep(1)   

    db_FS.close()
    print(">>===========================================\n")
    print('>> globas hscode list save End :' + str(now))
    os._exit(0)