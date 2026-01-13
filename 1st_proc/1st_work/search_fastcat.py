import requests
import re
import json

#상품코드로 검색엔진에 있는지 확인
def getSearchEngine(goodscode) :
    head = "".join(re.findall("[a-zA-Z]+",goodscode))
    guid = "".join(re.findall("\d+",goodscode))
    guid = guid.lstrip("0")
    
    site_list = {
        "G":"fashion","A":"auto","Y":"baby","E":"electron","F":"furniture","I":"industry","J":"jewelry","O":"office","S":"sports","B":"beauty",
        "CG":"fashion2","CA":"auto2","CY":"baby2","CE":"electron2","CF":"furniture2","CI":"industry2","CJ":"jewelry2","CO":"office2","CS":"sports2","CB":"beauty2",
        "Q":"usa","W":"mini","H":"handmade","X":"best","P":"shop","R":"ref","V":"global","K":"uk","D":"de","N":"mall","T":"trend","L":"cn","Z":"red"
    }
    
    site = site_list[head]
    
    url = "http://59.23.231.204:8090/service/search.json"    
    search_str = "{{goodscode:ALL({0}):100:15}}".format(goodscode)    
    params = {"cn":site,"fl":"uid,title,imgb,price,cate_idx,catecode,ali_no","se":search_str,"sn":1,"ln":10}
    
    res = requests.get(url,params=params)
    result = res.text     
    
    return result

#ali_no로 검색엔진 있는지 확인
def getSearchEngineAlicode(ali_no) :    
    
    site_list = ["fashion","auto","baby","electron","furniture","industry","jewelry","office","sports","beauty","fashion2","auto2","baby2","electron2","furniture2","industry2","jewelry2","office2","sports2","beauty2","red"]    
    site_str = ",".join(site_list)
    
    url = "http://59.23.231.204:8090/service/search.json"    
    search_str = "{{ali_no:ALL({0}):100:15}}".format(ali_no)    
    params = {"cn":site_str,"fl":"uid,goodscode,title,imgb,price,cate_idx,catecode,ali_no","se":search_str,"sn":1,"ln":10}
    
    res = requests.get(url,params=params)
    result = res.text     
    
    return result

#goodscode로 찾는 예제
#그냥 출력
print(getSearchEngine("S0007056705"))
#json으로 활용
print(json.loads(getSearchEngine("S0007056705")))



#ali_no로 찾는 예제
#그냥 출력
print(getSearchEngineAlicode("32299099944"))
#json으로 활용
print(json.loads(getSearchEngineAlicode("32299099944")))