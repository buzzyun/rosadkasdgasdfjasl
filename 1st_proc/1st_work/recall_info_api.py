import datetime
import func
import func_user
import sys, os
import request
import DBmodule_FR

global insCnt

def recall_api(serviceKey, menuID, page):
    rtnFlg = ""
    proc_url = "https://www.consumer.go.kr/openapi/recall/contents/index.do?serviceKey={}&pageNo={}&cntPerPage=100&cntntsId={}".format(serviceKey, page, menuID)
    req = request.get(proc_url)
    if req.status_code == 200:
        xmlStr = str(req.text)
        return xmlStr

    print(">> req.status_code : {}".format(req.status_code))
    print(">> req : {}".format(req))
    return rtnFlg


def repStr(targetStr):
    targetStr = targetStr.replace('<![CDATA[','').replace(']]>','').replace("'","")
    targetStr = str(targetStr)[:1000]
    return str(targetStr)


def getModelNo(tagetStr):
    modelNo = ""
    tagetStr = str(tagetStr)
    if str(tagetStr).find('(모델명 :') > -1:
        modelNo = func.getparse(tagetStr,'(모델명 :',')').strip()
    elif str(tagetStr).find('(모델명:') > -1:
        modelNo = func.getparse(tagetStr,'(모델명:',')').strip()
    elif str(tagetStr).find('(모델번호 :') > -1:
        modelNo = func.getparse(tagetStr,'(모델번호 :',')').strip()
    elif str(tagetStr).find('(모델번호:') > -1:
        modelNo = func.getparse(tagetStr,'(모델번호:',')').strip()
    elif str(tagetStr).find('(모델 :') > -1:
        modelNo = func.getparse(tagetStr,'(모델 :',')').strip()
    elif str(tagetStr).find('(모델:') > -1:
        modelNo = func.getparse(tagetStr,'(모델:',')').strip()
    elif str(tagetStr).find('(품번:') > -1:
        modelNo = func.getparse(tagetStr,'(품번:',')').strip()

    if modelNo == "":
        if str(tagetStr).find('o 모델 :') > -1:
            modelNo = func.getparse(tagetStr,'o 모델 :','').strip()
        elif str(tagetStr).find('o 모델번호 :') > -1:
            modelNo = func.getparse(tagetStr,'o 모델번호 :','').strip()
        # elif str(tagetStr).find('o 모델 / 연식 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o 모델 / 연식 :','').strip()
        elif str(tagetStr).find('o 모델/형식 :') > -1:
            modelNo = func.getparse(tagetStr,'o 모델/형식 :','').strip()
        # elif str(tagetStr).find('o EC 형식/모델 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o EC 형식/모델 :','').strip()
        # elif str(tagetStr).find('o EC 형식 승인/모델 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o EC 형식 승인/모델 :','').strip()
        # elif str(tagetStr).find('o 모델 / 카탈로그 번호 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o 모델 / 카탈로그 번호 :','').strip()
        # elif str(tagetStr).find('o 모델 및 색상 / 품목번호 /') > -1:
        #     modelNo = func.getparse(tagetStr,'o 모델 및 색상 / 품목번호 /','').strip()
        elif str(tagetStr).find('o 모델명/모델번호 :') > -1:
            modelNo = func.getparse(tagetStr,'o 모델명/모델번호 :','').strip()

        elif str(tagetStr).find('o 모델번호/UPC :') > -1:
            modelNo = func.getparse(tagetStr,'o 모델번호/UPC :','').strip()
        elif str(tagetStr).find('o 형식/모델번호 :') > -1:
            modelNo = func.getparse(tagetStr,'o 형식/모델번호 :','').strip()
        elif str(tagetStr).find('o 모델명 :') > -1:
            modelNo = func.getparse(tagetStr,'o 모델명 :','').strip()
        # elif str(tagetStr).find('o 모델/타입 : ') > -1:
        #     modelNo = func.getparse(tagetStr,'o 모델/타입 : ','').strip()
        # elif str(tagetStr).find('o 제품 / 품목번호 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o 제품 / 품목번호 :','').strip()
        # elif str(tagetStr).find('o 제품명 / 제품번호 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o 제품명 / 제품번호 :','').strip()
        # elif str(tagetStr).find('o 제품 / 모델번호 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o 제품 / 모델번호 :','').strip()
        # elif str(tagetStr).find('o 배터리 모델번호 : ') > -1:
        #     modelNo = func.getparse(tagetStr,'o 배터리 모델번호 : ','').strip()
        # elif str(tagetStr).find('o 제품번호 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o 제품번호 :','').strip()
        # elif str(tagetStr).find('o ASIN 번호 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o ASIN 번호 :','').strip()
        # elif str(tagetStr).find('o 로트번호 :') > -1:
        #     modelNo = func.getparse(tagetStr,'o 로트번호 :','').strip()
        # elif str(tagetStr).find('o ASIN :') > -1:
        #     modelNo = func.getparse(tagetStr,'o ASIN :','').strip()
        # elif str(tagetStr).find('o 모델 ') > -1:
        #     modelNo = func.getparse(tagetStr,'o 모델 ','').strip()
        # elif str(tagetStr).find('o모델명 ') > -1:
        #     modelNo = func.getparse(tagetStr,'o모델명 ','').strip()

        if modelNo != "":
            if str(modelNo).find(" o ") > -1:
                modelNo = func.getparse(modelNo,'',' o ').strip()
            elif str(modelNo).find("\no ") > -1:
                modelNo = func.getparse(modelNo,'','\no ').strip()
            elif str(modelNo).find("*") > -1:
                modelNo = func.getparse(modelNo,'','*').strip()
            elif str(modelNo).find("(") > -1:
                modelNo = func.getparse(modelNo,'','(').strip()
            # elif str(modelNo).find("\r\n\r") > -1:
            #     modelNo = func.getparse(modelNo,'','\r\n\r').strip()
            # elif str(modelNo).find("\n") > -1:
            #     modelNo = func.getparse(modelNo,'','\n').strip()

    return str(modelNo)[:1000]

def parsingProc(db_ali, xmlStr, menuID, page):
    global insCnt
    spList = xmlStr.split('<content>')
    for eaitem in spList:
        recallSn = func.getparse(eaitem, '<recallSn>', '</recallSn>')
        if recallSn == "":
            continue
        cntntsId = repStr(func.getparse(eaitem, '<cntntsId>', '</cntntsId>'))
        if str(cntntsId) != str(menuID):
            print(">> [{}] (SKIP) recallSn : {} | cntntsId : {}".format(page, recallSn, cntntsId))
            continue
        productNm = repStr(func.getparse(eaitem, '<productNm>', '</productNm>'))
        makr = repStr(func.getparse(eaitem, '<makr>', '</makr>'))
        bsnmNm = repStr(func.getparse(eaitem, '<bsnmNm>', '</bsnmNm>'))
        mnfcturPd = repStr(func.getparse(eaitem, '<mnfcturPd>', '</mnfcturPd>'))
        modlNmInfo = repStr(func.getparse(eaitem, '<modlNmInfo>', '</modlNmInfo>'))
        mnfcturNoInfo = repStr(func.getparse(eaitem, '<mnfcturNoInfo>', '</mnfcturNoInfo>'))
        stdBrcd = repStr(func.getparse(eaitem, '<stdBrcd>', '</stdBrcd>'))
        distbTmlmtDe = repStr(func.getparse(eaitem, '<distbTmlmtDe>', '</distbTmlmtDe>'))
        prmisnNo = repStr(func.getparse(eaitem, '<prmisnNo>', '</prmisnNo>'))
        mdlpClNo = repStr(func.getparse(eaitem, '<mdlpClNo>', '</mdlpClNo>'))
        aditfield13 = repStr(func.getparse(eaitem, '<aditfield13>', '</aditfield13>'))
        etcInfo = repStr(func.getparse(eaitem, '<etcInfo>', '</etcInfo>'))
        mainSleoffic = repStr(func.getparse(eaitem, '<mainSleoffic>', '</mainSleoffic>'))
        shrtcomCn = repStr(func.getparse(eaitem, '<shrtcomCn>', '</shrtcomCn>'))
        recallSe = repStr(func.getparse(eaitem, '<recallSe>', '</recallSe>'))
        recallPublictBgnde = repStr(func.getparse(eaitem, '<recallPublictBgnde>', '</recallPublictBgnde>'))
        recallPublictEndde = repStr(func.getparse(eaitem, '<recallPublictEndde>', '</recallPublictEndde>'))
        injryCauseResult = repStr(func.getparse(eaitem, '<injryCauseResult>', '</injryCauseResult>'))
        injryFrgltyTrgter = repStr(func.getparse(eaitem, '<injryFrgltyTrgter>', '</injryFrgltyTrgter>'))
        hrmflGrad = repStr(func.getparse(eaitem, '<hrmflGrad>', '</hrmflGrad>'))
        acdntCn = repStr(func.getparse(eaitem, '<acdntCn>', '</acdntCn>'))
        cnsmrGhvrTips = repStr(func.getparse(eaitem, '<cnsmrGhvrTips>', '</cnsmrGhvrTips>'))
        trtmntAtpn = repStr(func.getparse(eaitem, '<trtmntAtpn>', '</trtmntAtpn>'))
        recallBgnde = repStr(func.getparse(eaitem, '<recallBgnde>', '</recallBgnde>'))
        recallEndde = repStr(func.getparse(eaitem, '<recallEndde>', '</recallEndde>'))
        recallProcssInfo = repStr(func.getparse(eaitem, '<recallProcssInfo>', '</recallProcssInfo>'))
        recallEntrpsInfo = repStr(func.getparse(eaitem, '<recallEntrpsInfo>', '</recallEntrpsInfo>'))
        infoOriginInstt = repStr(func.getparse(eaitem, '<infoOriginInstt>', '</infoOriginInstt>'))
        infoOriginUrl = repStr(func.getparse(eaitem, '<infoOriginInsttUrl>', '</infoOriginInsttUrl>'))
        infoCreatInstt = repStr(func.getparse(eaitem, '<infoCreatInstt>', '</infoCreatInstt>'))
        infoCreatUrl = repStr(func.getparse(eaitem, '<infoCreatUrl>', '</infoCreatUrl>'))

        model_no = getModelNo(productNm)
        if model_no == "":
            model_no = getModelNo(aditfield13)

        if model_no != "":
            print(">> model _no : {}".format(model_no))
        searchinfo = productNm + ("\n") + bsnmNm +  ("\n") + modlNmInfo +  ("\n") + stdBrcd +  ("\n") + aditfield13 +  ("\n") + mainSleoffic
        searchinfo = str(searchinfo)[:2500]
        print(">> searchinfo _no : {}".format(searchinfo))

        search_detail = dict()
        search_detail['productNm'] = '[' + productNm + ']'
        search_detail['makr'] = '[' + makr + ']'
        search_detail['bsnmNm'] = '[' + bsnmNm + ']'
        search_detail['mnfcturPd'] = '[' + mnfcturPd + ']'
        search_detail['modlNmInfo'] = '[' + modlNmInfo + ']'
        search_detail['mnfcturNoInfo'] = '[' + mnfcturNoInfo + ']'
        search_detail['stdBrcd'] = '[' + stdBrcd + ']'
        search_detail['distbTmlmtDe'] = '[' + distbTmlmtDe + ']'
        search_detail['prmisnNo'] = '[' + prmisnNo + ']'
        search_detail['mdlpClNo'] = '[' + mdlpClNo + ']'
        search_detail['aditfield13'] = '[' + aditfield13 + ']'
        search_detail['etcInfo'] = '[' + etcInfo + ']'
        search_detail['mainSleoffic'] = '[' + mainSleoffic + ']'
        search_detail['shrtcomCn'] = '[' + shrtcomCn + ']'
        search_detail['recallSe'] = '[' + recallSe + ']'
        search_detail['recallPublictBgnde'] = '[' + recallPublictBgnde + ']'
        search_detail['recallPublictEndde'] = '[' + recallPublictEndde + ']'
        search_detail['injryCauseResult'] = '[' + injryCauseResult + ']'
        search_detail['injryFrgltyTrgter'] = '[' + injryFrgltyTrgter + ']'
        search_detail['hrmflGrad'] = '[' + hrmflGrad + ']'
        search_detail['acdntCn'] = '[' + acdntCn + ']'
        search_detail['cnsmrGhvrTips'] = '[' + cnsmrGhvrTips + ']'
        search_detail['trtmntAtpn'] = '[' + trtmntAtpn + ']'
        search_detail['recallBgnde'] = '[' + recallBgnde + ']'
        search_detail['recallEndde'] = '[' + recallEndde + ']'
        search_detail['recallProcssInfo'] = '[' + recallProcssInfo + ']'
        search_detail['recallEntrpsInfo'] = '[' + recallEntrpsInfo + ']'
        search_detail['infoOriginInstt'] = '[' + infoOriginInstt + ']'
        search_detail['infoOriginUrl'] = '[' + infoOriginUrl + ']'
        search_detail['infoCreatInstt'] = '[' + infoCreatInstt + ']'
        search_detail['infoCreatUrl'] = '[' + infoCreatUrl + ']'

        search_detail = str(search_detail)[:2500].replace("'","").replace("\r"," ").replace("\n"," ").strip()
        #print("search_detail : {}".format(search_detail))

        sql = "select recallSn, cntntsId from recall_info where recallSn = '{}' and cntntsId = '{}'".format(recallSn, cntntsId)
        row = db_ali.selectone(sql)
        if not row:
            sql_ins = " INSERT INTO recall_info (recallSn,cntntsId,productNm,makr,bsnmNm,mnfcturPd,modlNmInfo,mnfcturNoInfo,stdBrcd,distbTmlmtDe,prmisnNo,mdlpClNo,aditfield13,etcInfo,mainSleoffic,shrtcomCn,recallSe,recallPublictBgnde,recallPublictEndde,injryCauseResult,injryFrgltyTrgter,hrmflGrad,acdntCn,cnsmrGhvrTips,trtmntAtpn,recallBgnde,recallEndde,recallProcssInfo,recallEntrpsInfo,infoOriginInstt,infoOriginUrl,infoCreatInstt,infoCreatUrl,model_no, searchinfo, searchinfo_detail) \
                values ('" + str(recallSn) + "',\
                '" + str(cntntsId) + "', \
                '" + str(productNm) + "', \
                '" + str(makr) + "', \
                '" + str(bsnmNm) + "', \
                '" + str(mnfcturPd) + "', \
                '" + str(modlNmInfo) + "', \
                '" + str(mnfcturNoInfo) + "', \
                '" + str(stdBrcd) + "', \
                '" + str(distbTmlmtDe) + "', \
                '" + str(prmisnNo) + "', \
                '" + str(mdlpClNo) + "', \
                '" + str(aditfield13) + "', \
                '" + str(etcInfo) + "', \
                '" + str(mainSleoffic) + "', \
                '" + str(shrtcomCn) + "', \
                '" + str(recallSe) + "', \
                '" + str(recallPublictBgnde) + "', \
                '" + str(recallPublictEndde) + "', \
                '" + str(injryCauseResult) + "', \
                '" + str(injryFrgltyTrgter) + "', \
                '" + str(hrmflGrad) + "', \
                '" + str(acdntCn) + "', \
                '" + str(cnsmrGhvrTips) + "', \
                '" + str(trtmntAtpn) + "', \
                '" + str(recallBgnde) + "', \
                '" + str(recallEndde) + "', \
                '" + str(recallProcssInfo) + "', \
                '" + str(recallEntrpsInfo) + "', \
                '" + str(infoOriginInstt) + "', \
                '" + str(infoOriginUrl) + "', \
                '" + str(infoCreatInstt) + "', \
                '" + str(infoCreatUrl) + "', \
                '" + str(model_no) + "', \
                '" + str(searchinfo) + "', \
                '" + str(search_detail) + "' \
                ) "

            #print(">> sql_ins : {}".format(sql_ins))
            print(">> [{}] (Insert) recallSn : {} | cntntsId : {}".format(page, recallSn, cntntsId))
            db_ali.execute(sql_ins)
            insCnt = insCnt + 1
        else:
            print(">> [{}] ( DB 존재 (SKIP)) recallSn : {} | cntntsId : {}".format(page, recallSn, cntntsId))
        #     recallSn = row[0]
        #     cntntsId = row[1]

        #     sql_ups = " UPDATE recall_info set \
        #         productNm = '" + str(productNm) + "', \
        #         makr = '" + str(makr) + "', \
        #         bsnmNm = '" + str(bsnmNm) + "', \
        #         mnfcturPd = '" + str(mnfcturPd) + "', \
        #         modlNmInfo = '" + str(modlNmInfo) + "', \
        #         mnfcturNoInfo = '" + str(mnfcturNoInfo) + "', \
        #         stdBrcd = '" + str(stdBrcd) + "', \
        #         distbTmlmtDe = '" + str(distbTmlmtDe) + "', \
        #         prmisnNo = '" + str(prmisnNo) + "', \
        #         mdlpClNo = '" + str(mdlpClNo) + "', \
        #         aditfield13 = '" + str(aditfield13) + "', \
        #         etcInfo = '" + str(etcInfo) + "', \
        #         mainSleoffic = '" + str(mainSleoffic) + "', \
        #         shrtcomCn = '" + str(shrtcomCn) + "', \
        #         recallSe = '" + str(recallSe) + "', \
        #         recallPublictBgnde = '" + str(recallPublictBgnde) + "', \
        #         recallPublictEndde = '" + str(recallPublictEndde) + "', \
        #         injryCauseResult = '" + str(injryCauseResult) + "', \
        #         injryFrgltyTrgter = '" + str(injryFrgltyTrgter) + "', \
        #         hrmflGrad = '" + str(hrmflGrad) + "', \
        #         acdntCn = '" + str(acdntCn) + "', \
        #         cnsmrGhvrTips = '" + str(cnsmrGhvrTips) + "', \
        #         trtmntAtpn = '" + str(trtmntAtpn) + "', \
        #         recallBgnde = '" + str(recallBgnde) + "', \
        #         recallEndde = '" + str(recallEndde) + "', \
        #         recallProcssInfo = '" + str(recallProcssInfo) + "', \
        #         recallEntrpsInfo = '" + str(recallEntrpsInfo) + "', \
        #         infoOriginInstt = '" + str(infoOriginInstt) + "', \
        #         infoOriginUrl = '" + str(infoOriginUrl) + "', \
        #         infoCreatInstt = '" + str(infoCreatInstt) + "', \
        #         infoCreatUrl = '" + str(infoCreatUrl) + "', \
        #         model_no = '" + str(model_no) + "', \
        #         searchinfo = '" + str(searchinfo) + "', \
        #         searchinfo_detail = '" + str(search_detail) + "' \
        #         where recallSn = '{}' and cntntsId = '{}'".format(recallSn, cntntsId)

        #     #print(">> sql_ups : {}".format(sql_ups))
        #     print(">> [{}] (update) recallSn : {} | cntntsId : {}".format(page, recallSn, cntntsId))
        #     db_ali.execute(sql_ups)            

    return insCnt

if __name__ == '__main__':

    print(str(datetime.datetime.now()))
    db_ali = DBmodule_FR.Database('aliexpress')
    # 공산품 / 식품 / 축산물 / 의약품 / 화장품 / 의료기기 / 자동차 / 먹는물 / 해외리콜
    # menulist = ['0101','0201','0203','0204','0206','0207','0301','0403','0501']
    # apilist = ['Z6VXACWI7H','DRA3XXKB88','NDVQPRVR25','VOGYBTM3SD','559CFKEPBY','HERQCN01XL','M9AP9OKBOJ','LF1CGKXJPC','4PKPRBW4LI']
    menulist = ['0501']
    apilist = ['4PKPRBW4LI']
    insCnt = 0
    for pair in zip(menulist, apilist):
        print(">> pair : {} ".format(pair))
        allCnt = 0
        menuID = pair[0]
        apiKey = pair[1]

        page = 1
        print(">> [{}] menuID : {} --------------------------".format(page, menuID))
        xmlStr = recall_api(apiKey, menuID, page)
        if xmlStr == "":
            print(">> api Call Error : {}".format(menuID))
            break
        # if str(xmlStr).find('<cntntsId>' +str(menuID)+ '</cntntsId>') == -1:
        #     print(">> [{}] menuID : {} 해당 데이터 없음 Skip ".format(page, menuID))
        #     continue

        allCnt = func.getparse(xmlStr, '<allCnt>', '</allCnt>')
        code = func.getparse(xmlStr, '<code>', '</code>')
        codeMsg = func.getparse(xmlStr, '<codeMsg>', '</codeMsg>')
        if code != "00":
            print(">> code : {} | codeMsg : {}".format(code, codeMsg))
            continue
        parsingProc(db_ali, xmlStr, menuID, page)

        roofCnt = int(allCnt) / 100
        page = page + 1
        while page < roofCnt:
            print("\n\n>> [{}] menuID : {} --------------------------".format(page, menuID))
            xmlStr = recall_api(apiKey, menuID, page)
            if xmlStr == "":
                print(">> api Call Error (2) : {}".format(menuID))
                break
            if str(xmlStr).find('<cntntsId>' +str(menuID)+ '</cntntsId>') == -1:
                print(">> [{}] menuID : {} 해당 데이터 없음 Skip (2)".format(page, menuID))
                page = page + 1
                continue
            else:
                parsingProc(db_ali, xmlStr, menuID, page)
                page = page + 1

    db_con = DBmodule_FR.Database('freeship')
    func_user.procLogSet(db_con, "recall_info", "P", insCnt, "Recall info (API) : " +str(insCnt))
    db_con.close()
    db_ali.close()

    print(str(datetime.datetime.now()))
    os._exit(0)
