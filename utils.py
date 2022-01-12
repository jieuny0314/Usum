import random, string
from datetime import datetime
from app import User, TransHistory
from sqlalchemy import and_, or_

BankType = {'농협은행':'011', '농협상호금융':'012', '산업은행':'002', '기업은행':'003', '국민은행':'004', 'KEB하나은행':'081',\
	'우리은행':'020', 'SC제일은행':'023', '시티은행':'027', '새마을금고':'045', '신한은행':'088', '카카오뱅크':'090'}

def makeCode():
    letters = string.ascii_lowercase+'0123456789'
    result_str = ''.join(random.choice(letters) for i in range(10))
    return result_str

def str2datetime(user_str, date=0):
	y = int(user_str[0:4])
	m = int(user_str[4:6])
	d = int(user_str[6:])
	return datetime(y,m,d)

def getCoupleTotal(connCode, date='12'):
	res = 0
	his = TransHistory.query.filter_by(connCode=connCode).all()

	for data in his:
		if len(date) == 8:
			if data.Trdd.strftime("%Y%m%d") == date:
				res = res+int(data.Usam)

		else:
			if data.Trdd.strftime("%m") == date:
				res = res+int(data.Usam)
	return res

def getUserTotal(user, date=''):
	res = 0
	his = TransHistory.query.filter_by(username=user).all()
	
	for data in his:
		if len(date)==8:
			if data.Trdd.strftime("%Y%m%d") == date:
				res = res+int(data.Usam)
		else:
			if data.Trdd.strftime("%m") == date:
				res = res+int(data.Usam)
	return res

def getCateTotal(category):
	his = TransHistory.query.filter_by(Category=category).all()
	res = 0
	for data in his:
		res = res+int(data.Usam)
	return res

def Total2Percent(total, a_total):
	return round((total / a_total) * 100)

