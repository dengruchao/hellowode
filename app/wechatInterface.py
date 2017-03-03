import requests
import json
import time
import pylibmc as memcache

class WechatInterface:

	def __init__(self):
		self.appId = 'wx7e49057f2b9ea954'
		self.secret = '37b4d4160ba04506f19958530c49a834'
		self.base_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}'

	def getAccessToken(self):
		mc = memcache.Client()
		token = mc.get('token')
		if token == None:
			print 'get access token'
			url = self.base_url.format(grant_type='client_credential', appid=self.appId, secret=self.secret)
			resp = requests.get(url)
			resp_json = json.loads(resp.content)
			access_token = resp_json['access_token']
			expires_in = resp_json['expires_in']
			mc.set('token', access_token, expires_in)
			token = mc.get('token')
		return token

	def addTempImg(self, filename):
		access_token = self.getAccessToken()
		url = "https://api.weixin.qq.com/cgi-bin/media/upload"
		payload_img = {'access_token': access_token, 'type': 'image'}
		data = {'media': open(filename, 'rb')}
		resp = requests.post(url=url, params=payload_img, files=data)
		print resp.content
		if resp.status_code == 200:
			resp_json = json.loads(resp.content)
			return resp_json['media_id']

wechatInterface = WechatInterface()
