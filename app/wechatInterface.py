import requests
import json

class WechatInterface:

	def __init__(self):
		self.appId = 'wx7e49057f2b9ea954'
		self.secret = '37b4d4160ba04506f19958530c49a834'
		self.base_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}'

	def getAccessToken(self):
		url = self.base_url.format(grant_type='client_credential', appid=self.appId, secret=self.secret)
		resp = requests.get(url)
		resp_json = json.loads(resp.content)
		return resp_json['access_token'], resp_json['expires_in']

wechatInterface = WechatInterface()
