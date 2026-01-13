import datetime
import re
import func_ali_new
import ali_option


def has_duplicates(seq):
    return len(seq) != len(set(seq))

if __name__ == '__main__':
    now = datetime.datetime.now()
    print('>> [--- main Proc start ---] ' + str(now))

    opt_source = ali_option.option_html
    ord_optionstr = "(201452272:203221806)VINYL-220X150CM:PEACOCK BLUE,수량:1(옵션가:11745)" # 옵션2개

    opt_source = ali_option.option_html2
    ord_optionstr = "(200005376:200006151)30X45CM NO FRAME:STYLE-6" # 품절있음 https://ko.aliexpress.com/item/1005005882341362.html?gatewayAdapt=glo2kor

    opt_source = ali_option.option_html3
    ord_optionstr = "(203008818:4182)Black Blue:XXL" # 중복옵션 https://ko.aliexpress.com/item/1005006328845966.html?gatewayAdapt=glo2kor
    
    
    edit_option = func_ali_new.option_dist(ord_optionstr)
    if edit_option == "S01" or edit_option == "S04":
        print(" (확인필요) after : {}".format(edit_option))
    else:
        print(">> (주문) Edit Option : {}".format(edit_option))

    dicOpt = dict()
    option_code = ""
    option_name = ""
    if edit_option == "":
        print(">> 옵션 없는 상품 ")
        dicOpt['code'] = ""
        dicOpt['name'] = ""
    else:
        if edit_option.find("(") > -1:
            opt_tmp = func_ali_new.getparse(edit_option,"(","").strip()
            if opt_tmp.find("(") > -1:
                #flg_search = "S01"  # SKIP
                print(">>  예전 옵션 (괄호 중복 1개이상 ) : {}".format(opt_tmp))
                #return flg_search

            option_code = func_ali_new.getparse(edit_option,"(",")").strip()
            option_name = func_ali_new.getparse(edit_option,")","").strip()
            if option_name[-1:] == ":":
                option_name = option_name[:-1]
            if option_name.find("(") > -1:
                #flg_search = "S01"  # SKIP
                print(">>  예전 옵션 (괄호 중복 1개이상 ) : {}".format(edit_option))
                #return flg_search

            sp_opt_code = option_code.split(":")
            sp_opt_name = option_name.split(":")

        dicOpt['code'] = option_code
        dicOpt['name'] = option_name.replace("  "," ").strip()
        print(" dicOpt : {}".format(dicOpt))

        sp_opt_title = opt_source.split('class="sku-item--property')
        sp_opt_title_cnt = len(sp_opt_title)
        ali_opt_cnt = len(sp_opt_title) -1

        i = 0
        cnt_opt_match = 0
        while i < ali_opt_cnt:
            title_name = func_ali_new.getparse(sp_opt_title[i+1],'class="sku-item--title--','<div>')
            title_name = func_ali_new.getparse(title_name,'<span>','<span>').replace(":","")
            option_coltmp = func_ali_new.getparse(sp_opt_title[i+1],'class="sku-item--skus--','')
            print("\n>>[{}] title_name : {}".format(i+1, title_name))
            sp_opt_col = option_coltmp.split('</div>')
            opt_name_list = []
            for ea_col in sp_opt_col:
                ea_opt_name = ""
                if ea_col.find('data-sku') == -1:
                    continue
                ea_opt_code_tmp = func_ali_new.getparse(ea_col,'data-sku-col="','"')
                ea_opt_code = ea_opt_code_tmp.split('-')[1]
                ea_opt_class = func_ali_new.getparse(ea_col,'class="','"')
                if ea_col.find('title="') > -1:
                    ea_opt_name = func_ali_new.getparse(ea_col,'title="','"')
                elif ea_col.find('alt="') > -1:
                    ea_opt_name = func_ali_new.getparse(ea_col,'alt="','"')
                else:
                    print(">> Option Name check ")
                opt_name_list.append(ea_opt_name)

                if ea_opt_class.find('soldOut') > -1:
                    print(">>[{}] (soldOut) ea_opt_code : {} | ea_opt_name : {} | class : {}".format(i+1, ea_opt_code, ea_opt_name, ea_opt_class))
                else:
                    print(">>[{}] ea_opt_code : {} | ea_opt_name : {} | class : {}".format(i+1, ea_opt_code, ea_opt_name, ea_opt_class))
                    if sp_opt_code[i] == ea_opt_code:
                        print(">> Opttion Code Match : {} | {}".format(sp_opt_code[i], ea_opt_code))
                        if sp_opt_name[i].strip().upper() == ea_opt_name.strip().upper():
                            print(">> Opttion Name Match : {} | {}".format(sp_opt_name[i], ea_opt_name))
                            cnt_opt_match = cnt_opt_match + 1 # 매칭 옵션이 있을경우
                            if ea_opt_class.find('selected') > -1:
                                print(">> Option selected ")
                            else:
                                print(">> Option Click Please ")
            i = i + 1
            if has_duplicates(opt_name_list) == True:
                print(">> 중복옵션명 있음 : ")
                print('>> [S06] 중복 옵션명 있음 (확인필요) ')
            else:
                print(">> 중복옵션명 없음 : ")

        if cnt_opt_match == ali_opt_cnt:
            print(">> Option Matching : {} | {} | {}".format(option_code, option_name, dicOpt['name']))
        else:
            print(">> Option Not Matching : 매칭cnt : {} | 옵션수 : {}".format(cnt_opt_match, ali_opt_cnt))


    print(">> ")