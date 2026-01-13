import func_user

input_file = input(">> Input File :")
# if input_file == "":
#     input_file = r"C:\Temp\temp.txt"

# with open 구문 포맷
with open(input_file, "r", encoding='UTF-8') as f:
    file_list = f.read()
    f.close()

sp_list = file_list.split("</tr>")
for ea_item in sp_list:
    if ea_item.find('freeship.co.kr') > -1:
        goods_url = func_user.getparse(ea_item, 'freeship.co.kr','" ')
        goods_url = "https://freeship.co.kr" + str(goods_url)
        goods_url = goods_url.replace('amp;','')
        if goods_url != "":
            print(goods_url)

input(">> End : ")