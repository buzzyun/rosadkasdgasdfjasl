def DbAccount(site):
	if site == 'handmade' or site == 'HANDMADE':
		SERVER = '59.23.231.202,14103'
		DATABASE = 'handmade2'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@admin#db1011'
	elif site == 'naver_price' or site == 'NAVER_PRICE':
		SERVER = '211.195.9.71,14103'
		DATABASE = 'naver_price'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@admin#db1011'
	elif site == 'taobao' or site == 'TAOBAO':
		SERVER = '211.195.9.69,14103'
		DATABASE = 'cn'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@admin#db1011'
	elif site == 'shop' or site == 'SHOP':
		SERVER = '211.195.9.69,14103'
		DATABASE = 'shop'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@admin#db1011'
	elif site == 'freeship':
		SERVER = '59.23.231.194,14103'
		DATABASE = 'freeship'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@allin#am1071'
	elif site == 'aliexpress':
		SERVER = '59.23.231.194,14103'
		DATABASE = 'aliexpress'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@allin#am1071'

	info = {"db":DATABASE,"host":SERVER,"user":USERNAME,"password":PASSWORD}
	return info
