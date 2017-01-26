import requests
import json
import pyquery
import time
import traceback

import Browser

class Login(object): 

	def __init__(self, prefix):
		self.prefix = prefix
		self.urlLoginInit = 'http://' + self.prefix + '.minghuaetc.com/home/login.mooc'
		self.urlDoLogin = 'http://' + self.prefix + '.minghuaetc.com/home/doLogin.mooc'


	def login(self, userName, password):

		try:
			st = time.time()

			browser = Browser.Browser()
			j = pyquery.PyQuery(
				browser.session.get(self.urlLoginInit).content
			)
				
			strToken = self.getEncryptPwd(
				password, 
				j('#tokenId').val(), 
				j('#modulus').val(), 
				j('#exponent').val(), 
				''
			)


			res = browser.session.post(self.urlDoLogin, data = {
				'loginName' : userName,
				'strToken' : strToken,
				'loginType' : 0,
				'isCheckCode' : 0,
				'historyUrl' : ''
			})

			self.saveUserInfo(userName, password, strToken, self.prefix)

			et = time.time()
			LogUtil.getLogger(userName, 'login').info('[login success cost : ' + str(et-st) + ']')

			return json.loads(res.text), browser
		except Exception, err:
			LogUtil.getLogger(userName, 'login.fatal').error('[login fail]')


	def getEncryptPwd(self, pwd, tokenId, modulus, exponent, time):

		urlGetEncryptPwd = 'http://cp01-ocean-1901.epc.baidu.com:8888/'
		urlGetEncryptPwd += '?pwd=' + pwd
		urlGetEncryptPwd += '&tokenId=' + tokenId
		urlGetEncryptPwd += '&modulus=' + modulus
		urlGetEncryptPwd += '&exponent=' + exponent


		if time != None and time != '':
			urlGetEncryptPwd += '&time=' + time

		return requests.get(urlGetEncryptPwd).content


	def saveUserInfo(self, userName, password, token, school):
		url = 'http://cp01-ocean-1901.epc.baidu.com:8080/sae/index.php/minghuaUserInfo/addItem'

		data = {}
		data['user_name'] = userName
		data['password'] = password
		data['token'] = token
		data['school'] = school
		requests.post(url, data = data)


	def getUserInfo(self, userName):
		url = 'http://cp01-ocean-1901.epc.baidu.com:8080/sae/index.php/minghuaUserInfo/getItem'
		data = {}
		data['user_name'] = userName
		return json.loads(requests.post(url, data=data).content)
