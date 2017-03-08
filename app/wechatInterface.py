# -*- coding: utf-8 -*-
import requests
import json
import pylibmc as memcache

class WechatInterface:

    def __init__(self):
        #self.appId = 'wx7e49057f2b9ea954'
        #self.secret = '37b4d4160ba04506f19958530c49a834'
        self.appId = 'wx928c1d7848868b7e'
        self.secret = '7200e771bf65a8a6145dee9372ddcd9e'
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

    def addMedia(self, filename, type, temp):
        access_token = self.getAccessToken()
        if temp:
            url = "https://api.weixin.qq.com/cgi-bin/media/upload"
        else:
            url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
        payload_img = {'access_token': access_token, 'type': type}
        data = {'media': open(filename, 'rb')}
        resp = requests.post(url=url, params=payload_img, files=data)
        if resp.status_code == 200:
            resp_json = json.loads(resp.content)
            return resp_json['media_id']

    def getMediaList(self, type, offset=0, count=20):
        access_token = self.getAccessToken()
        url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material"
        payload_img = {'access_token': access_token, 'type': type}
        resp = requests.post(url=url, params=payload_img)
        if resp.status_code == 200:
            resp_json = json.loads(resp.content)
            print resp_json['item']
            return 'success'

    def menuCreate(self):
        access_token = self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
        payload = {
                    "button":[
                        {
                            "type":"click",
                            "name":u"今日歌曲",
                            "key":"V1001_TODAY_MUSIC"
                        },
                        {
                            "name":u"菜单",
                            "sub_button":[
                            {
                                "type":"view",
                                "name":u"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":u"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":u"赞一下我们",
                                "key":"V1001_GOOD"
                            }]
                        }]
                    }
        resp = requests.post(url=url, params=payload)
        if resp.status_code == 200:
            print 'ok'

wechatInterface = WechatInterface()
