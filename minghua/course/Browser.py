import requests

class Browser: 

	def __init__(self):
		print('in Browser')
		self.session = requests.Session()
		headers = {
			'Accept' : '*/*',
			'Accept-Encoding' : 'deflate',
			'Accept-Language' : 'zh-CN,zh;q=0.8',
			'Cache-Control' : 'no-cache',
			'Connection' : 'keep-alive',
			'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
			'Pragma' : 'no-cache',
			'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727	)',
			'X-Requested-With' : 'XMLHttpRequest'
		}
		self.session.headers.update(headers)