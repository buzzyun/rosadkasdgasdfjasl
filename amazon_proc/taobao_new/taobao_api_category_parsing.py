
import datetime
import taobao_api_cate_source

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

    print('>> [--- main start ---] ' + str(datetime.datetime.now()))
    row = 0
    catecode_auto = 50000
    cate_source = taobao_api_cate_source.category_api_source
    cate_tmp = getparse(cate_source,'<div class="categories-list__wrap">','')
    sp_bcate = cate_source.split('<div class="categories-list__wrap">')
    for b_cate in sp_bcate:
        b_cate_name = getparse(b_cate, '<h3>', '</h3>')
        middle_cate = getparse(b_cate, '<ul>', '</ul>')

        catecode_auto = catecode_auto + 1
        sp_mcate = middle_cate.split('</li>')
        for m_cate in sp_mcate:
            m_cate_name = getparse(m_cate, '<a href="', '</a>')
            m_cate_name = getparse(m_cate_name, '>', '').strip()
            m_cate_url = getparse(m_cate, '<a href="', '"').replace('amp;','').strip()
            m_cate_url = "https://open-demo.otcommerce.com" + str(m_cate_url)
            if m_cate_url != "":
                row = row + 1
                print(">> ({}) [{}] {} >> {} | {}".format(row, catecode_auto, b_cate_name, m_cate_name, m_cate_url))
        print("\n\n>> ============================================ ")
    print(">> End ")