
from datetime import datetime, timedelta

now = datetime.now()
print("현재 :", now)	# 현재 : 2021-01-09 21:51:33.170644

date_to_compare = datetime.strptime("20240421", "%Y%m%d")
print("비교할 날짜 :", date_to_compare)	# 비교할 날짜 : 2020-12-25 00:00:00

diff = now - date_to_compare
print("차이 :", diff, ", Type :", type(diff))	

yesterday = now - diff 
yesterday = yesterday.strftime("%Y.%m.%d")
print(yesterday)

for i in range(131, 0, -1):
  diff = timedelta(days=i)
  
  yesterday = now - diff
  yesterday = yesterday.strftime("%Y.%m.%d")
  print(">> diff( {} ) : {}".format(i, yesterday))



print(yesterday)

