import requests
import json
import pyquery
import time
import traceback

from minghua.course.Browser import Browser

class Login(object):

	def __init__(self, prefix):
		self.prefix = prefix
		self.urlLoginInit = 'http://' + self.prefix + '.minghuaetc.com/home/login.mooc'
		self.urlDoLogin = 'http://' + self.prefix + '.minghuaetc.com/home/doLogin.mooc'

	def login(self, userName, password):

		try:
			#st = time.time()

			# print(self.prefix)
			# print(userName)
			# print(password)

			browser = Browser()
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

			#print(strToken)

			res = browser.session.post(self.urlDoLogin, data = {
				'loginName' : userName,
				'strToken' : strToken,
				'loginType' : 0,
				'isCheckCode' : 0,
				'historyUrl' : ''
			})

			#print(res.content)

			#self.saveUserInfo(userName, password, strToken, self.prefix)

			#et = time.time()
			#LogUtil.getLogger(userName, 'login').info('[login success cost : ' + str(et-st) + ']')

			return json.loads(res.text), browser
		except Exception as err:
			traceback.print_exc()
			#LogUtil.getLogger(userName, 'login.fatal').error('[login fail]')


	def getEncryptPwd(self, pwd, tokenId, modulus, exponent, time):

		urlGetEncryptPwd = 'http://116.62.10.40:8888/'
		urlGetEncryptPwd += '?pwd=' + pwd
		urlGetEncryptPwd += '&tokenId=' + tokenId
		urlGetEncryptPwd += '&modulus=' + modulus
		urlGetEncryptPwd += '&exponent=' + exponent


		if time != None and time != '':
			urlGetEncryptPwd += '&time=' + time

		return requests.get(urlGetEncryptPwd).content