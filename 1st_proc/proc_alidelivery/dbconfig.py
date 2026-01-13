def DbAccount(site):
	if site == 'taobao':
		SERVER = '211.195.9.69:14103'
		DATABASE = 'cn'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@admin#db1011'
	elif site == 'freeship':
		SERVER = '59.23.231.194:14103'
		DATABASE = 'freeship'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@allin#am1071'
	elif site == 'aliexpress':
		SERVER = '59.23.231.194:14103'
		DATABASE = 'aliexpress'
		USERNAME = '1stplatfor_sql'
		PASSWORD = '@allin#am1071'

	info = {"db":DATABASE,"host":SERVER,"user":USERNAME,"password":PASSWORD}
	return info
