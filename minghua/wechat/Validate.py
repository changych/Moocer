import haslib

class Validate(object):

	def validate(self, signature, timestmp, nonce):
		token = '715074363yuan'
		params = [token, timestmp, nonce]
		rawStr = ''.join(params)
		shaStr = hashlib.sha1(rawStr).hexdigest()
		if shaStr == signature:
			return True
		else:
			return False