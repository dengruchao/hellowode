import requests
import json
import time


class WechatInterface:

	def __init__(self):
		self.appId = 'wx7e49057f2b9ea954'
		self.secret = '37b4d4160ba04506f19958530c49a834'
		self.base_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}'
		self.getAccessToken()

	def getAccessToken(self):
		print 'get access token'
		url = self.base_url.format(grant_type='client_credential', appid=self.appId, secret=self.secret)
		resp = requests.get(url)
		resp_json = json.loads(resp.content)
		self.access_token = resp_json['access_token']
		self.expires_in = resp_json['expires_in']
		self.get_token_time = time.time()

	def checkAccessToken(self):
		now_time = time.time()
		if abs(now_time - self.get_token_time) > 7000:
			self.getAccessToken()

	def addTempImg(self, filename):
		self.checkAccessToken()
		url = "https://api.weixin.qq.com/cgi-bin/media/upload"
		payload_img = {'access_token': self.access_token, 'type': 'image'}
		data = {'media': open(filename, 'rb')}
		resp = requests.post(url=url, params=payload_img, files=data)
		print resp
		if resp.status_code == 200:
			resp_json = json.loads(resp.content)
			return resp_json['media_id']

wechatInterface = WechatInterface()
