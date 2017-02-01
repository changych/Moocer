#-*- coding: utf-8 -*-  
import hashlib

class Validate(object):

	def validate(self, signature, timestmp, nonce):
		token = '715074363yuan'
		params = [token, timestmp, nonce]
		params.sort()
		rawStr = ''.join(params)
		print(rawStr)
		shaStr = hashlib.sha1(rawStr.encode('utf-8')).hexdigest()
		print(shaStr)
		if shaStr == signature:
			return True
		else:
			return shaStr