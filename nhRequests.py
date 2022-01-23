import requests, json, datetime, random

URL = {}
URL['origin'] = 'https://developers.nonghyup.com/'
URL['OpenFinAccountDirect'] = URL['origin'] + 'OpenFinAccountDirect.nh'
URL['CheckOpenFinAccountDirect'] = URL['origin'] + 'CheckOpenFinAccountDirect.nh'
URL['OpenFinCard'] = URL['origin'] + 'OpenFinCardDirect.nh'
URL['OpenFinCardDirect'] = URL['origin'] + 'CheckOpenFinCardDirect.nh'
URL['CardHistoryURL'] = URL['origin'] + 'InquireCreditCardAuthorizationHistory.nh'
URL['send2accNum'] = URL['origin'] + 'ReceivedTransferAccountNumber.nh'
URL['ReceivedTransferOtherBank'] = URL['origin'] + 'ReceivedTransferOtherBank.nh'
URL['InquireBalance'] = URL['origin'] + 'InquireBalance.nh'
URL['InquireDepositorAccountNumber'] = URL['origin'] + 'InquireDepositorAccountNumber.nh'
URL['InquireDepositorOtherBank'] = URL['origin'] + 'InquireDepositorOtherBank.nh'
URL['DrawingTransfer'] = URL['origin'] + 'DrawingTransfer.nh'

headers = {'Content-Type': 'application/json;charset=utf-8', 'accept':'application/json;'}
Iscd = '000489'
AccessToken = '81af5ea0e939de973f9a90101beb76576a9df7cf4585049c9309c5d0c2b5c943'
TestFincard = '00829101234560000112345678919'
TestFinaccount = '00820100004890000000000004428'

def getIsTuno():
	return getNow('date')+getNow('time')+str(random.randint(10000, 99999))

def getNow(input):
	now = datetime.datetime.now()
	if input=='date':
		return str(now.strftime('%Y%m%d'))

	else:
		return str(now.strftime('%H%M%S'))

def getFinAccount(Brdt, Bncd, Acno):
	jsondata = {
	    "Header": {
	        "ApiNm": "OpenFinAccountDirect",
	        "Tsymd": getNow('date'),
	        "Trtm": getNow('time'),
	        "Iscd": Iscd,
	        "FintechApsno": "001",
	        "ApiSvcCd": "DrawingTransferA",
	        "IsTuno": getIsTuno(),
	        "AccessToken": AccessToken
	    },
	    "DrtrRgyn": "Y",
	    "BrdtBrno": Brdt,
	    "Bncd": Bncd,
	    "Acno": Acno
	}
	res = requests.post(URL['OpenFinAccountDirect'], headers=headers, data=json.dumps(jsondata))
	res_data = json.loads(res.text)
	print(res_data)

	jsondata = {	
	  "Header":{
	    "ApiNm":"CheckOpenFinAccountDirect",
	    "Tsymd":getNow('date'),
	    "Trtm":getNow('time'),
	    "Iscd":Iscd,
	    "FintechApsno":"001",
	    "ApiSvcCd":"DrawingTransferA",
	    "IsTuno":getIsTuno(),
	    "AccessToken": AccessToken
	  },
	  "Rgno":res_data['Rgno'],
	  "BrdtBrno":Brdt 
	}
	res = requests.post(URL['CheckOpenFinAccountDirect'], headers=headers, data=json.dumps(jsondata))
	res_data = json.loads(res.text)

	print(res_data)

def getFinCard(Brdt, Cano):
	jsondata = {	
	    "Header":{
	        "ApiNm":"OpenFinCardDirect",
	        "Tsymd":getNow('date'),
	        "Trtm":getNow('time'),
	        "Iscd":Iscd,
	        "FintechApsno":"001",
	        "ApiSvcCd":"DrawingTransferA",
	        "IsTuno":getIsTuno(),
	        "AccessToken": AccessToken
	    },
	"Brdt":Brdt,
	"Cano":Cano 
	}
	res = requests.post(URL['OpenFinCard'], headers=headers, data=json.dumps(jsondata))
	res_data = json.loads(res.text)
	print(res_data)
	print('\n')
	jsondata = {	
	    "Header":{
	        "ApiNm":"CheckOpenFinCardDirect",
	        "Tsymd":getNow('date'),
	        "Trtm":getNow('time'),
	        "Iscd":Iscd,
	        "FintechApsno":"001",
	        "ApiSvcCd":"DrawingTransferA",
	        "IsTuno":getIsTuno(),
	        "AccessToken": AccessToken
	    },
	"Rgno":res_data['Rgno'],
	"Brdt":Brdt,
	}
	res = requests.post(URL['OpenFinCardDirect'], headers=headers, data=json.dumps(jsondata))
	res_data = json.loads(res.text)
	return res_data['FinCard']

def getAccoMoney(FinAcno):
	jsondata = {
	    "Header": {
	        "ApiNm": "InquireBalance",
	        "Tsymd": getNow('date'),
	        "Trtm": getNow('time'),
	        "Iscd": Iscd,
	        "FintechApsno": "001",
	        "ApiSvcCd": "ReceivedTransferA",
	        "IsTuno": getIsTuno(),
	        "AccessToken": AccessToken
	    },
	    "FinAcno": FinAcno
	}
	res = requests.post(URL['InquireBalance'], headers=headers, data=json.dumps(jsondata))
	res_data = json.loads(res.text)
	print(res_data)

def getCardUseHistory(debug=False):
	if debug == True:
		with open('testHistory.json') as json_file:
			res_data = json.load(json_file)

	else:
		jsondata = {	
		    "Header":{
		        "ApiNm":"InquireCreditCardAuthorizationHistory",
		        "Tsymd":getNow('date'),
		        "Trtm":getNow('time'),
		        "Iscd":Iscd,
		        "FintechApsno":"001",
		        "ApiSvcCd":"CardInfo",
		        "IsTuno":getIsTuno(),
		        "AccessToken": AccessToken
		    },
		"FinCard": TestFincard,
	    "IousDsnc": "1",
	    "Insymd": "20191105",
	    "Ineymd": "20191109",
	    "PageNo": "1",
	    "Dmcnt": "15"
		}
		res = requests.post(URL['CardHistoryURL'], headers=headers, data=json.dumps(jsondata))
		res_data = json.loads(res.text)

	return res_data

def Trans2Usum(FinAcno, Tram, DractOtlt, MractOtlt):#핀-어카운트 등록계좌 --> 모계좌
	jsondata = {	
	    "Header":{
	        "ApiNm":"DrawingTransfer",
	        "Tsymd":getNow('date'),
	        "Trtm":getNow('time'),
	        "Iscd":Iscd,
	        "FintechApsno":"001",
	        "ApiSvcCd":"DrawingTransferA",
	        "IsTuno":getIsTuno(), 
	        "AccessToken": AccessToken
	    },
	  "FinAcno":FinAcno,
	  "Tram":Tram,
	  "DractOtlt":DractOtlt,
	  "MractOtlt":MractOtlt
	}

	res = requests.post(URL['DrawingTransfer'], headers=headers, data=json.dumps(jsondata))
	res_data = json.loads(res.text)
	print(res_data)

def send2accNum(Bncd, Acno, Tram, DractOtlt, MractOtlt):#모계좌 --> 입력계좌
	jsondata = {
	  "Header":{
	      "ApiNm":"ReceivedTransferAccountNumber",
	      "Tsymd":getNow('date'),
	      "Trtm":getNow('time'),
	      "Iscd":Iscd,
	      "FintechApsno":"001",
	      "ApiSvcCd":"ReceivedTransferA",
	      "IsTuno":getIsTuno(),
	      "AccessToken":AccessToken
	      },
	  "Bncd":Bncd,
	  "Acno":Acno,
	  "Tram":Tram,
	  "DractOtlt":DractOtlt,
	  "MractOtlt":MractOtlt 
	}
	if (Bncd != '011') and (Bncd != '012'):
		jsondata['Header']['ApiNm'] = "ReceivedTransferOtherBank"
		res = requests.post(URL['ReceivedTransferOtherBank'], headers=headers, data=json.dumps(jsondata))
		res_data = json.loads(res.text)
		print(res_data)
	else:
		res = requests.post(URL['send2accNum'], headers=headers, data=json.dumps(jsondata))
		res_data = json.loads(res.text)
		print(res_data)

def getAccountOwnerNm(chkNH, Bncd, Acno):
	jsondata = {
	    "Header":{
	        "ApiNm":"InquireDepositorAccountNumber",
	        "Tsymd":getNow('date'),
	        "Trtm":getNow('time'),
	        "Iscd":Iscd,
	        "FintechApsno":"001",
	        "ApiSvcCd":"DrawingTransferA",
	        "IsTuno":getIsTuno(),
	        "AccessToken":
	        AccessToken
	        },
	        "Bncd":Bncd,
	        "Acno":Acno                
	}
	if chkNH == True:
		res = requests.post(URL['InquireDepositorAccountNumber'], headers=headers, data=json.dumps(jsondata))
		
	else:
		jsondata['Header']['ApiNm'] = 'InquireDepositorOtherBank'
		res = requests.post(URL['InquireDepositorOtherBank'], headers=headers, data=json.dumps(jsondata))
	
	res_data = json.loads(res.text)
	print(res_data) 
