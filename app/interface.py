# -*- coding: utf-8 -*-
import requests
import json
import os
import pickle
import time

class Interface:

    def __init__(self):
        self.appId = 'wx7e49057f2b9ea954'
        self.secret = '37b4d4160ba04506f19958530c49a834'
        #self.appId = 'wx928c1d7848868b7e'
        #self.secret = '7200e771bf65a8a6145dee9372ddcd9e'
        self.base_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}'

    def getAccessToken(self):
        if os.path.exists('app/static/token.pkl'):
            with open('app/static/token.pkl') as f:
                token = pickle.load(f)
            expires_in = token['expires_in']
            time1 = token['time1']
            time2 = time.time()
            if time2 - time1 >= expires_in-10:
                token = None
        else:
            token = None

        if token == None:
            print 'get access token'
            url = self.base_url.format(grant_type='client_credential', appid=self.appId, secret=self.secret)
            resp = requests.get(url)
            resp_json = json.loads(resp.content)
            access_token = resp_json['access_token']
            expires_in = resp_json['expires_in']
            token = {'access_token': access_token, 'expires_in': expires_in, 'time1': time.time()}
            with open('app/static/token.pkl', 'wb') as f:
                pickle.dump(token, f)

        access_token = token['access_token']
        return access_token

    def addMedia(self, filename, media_type, temp):
        access_token = self.getAccessToken()
        if temp:
            url = "https://api.weixin.qq.com/cgi-bin/media/upload"
        else:
            url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
        payload_img = {'access_token': access_token, 'type': media_type}
        data = {'media': open(filename, 'rb')}
        resp = requests.post(url=url, params=payload_img, files=data)
        if resp.status_code == 200:
            resp_json = json.loads(resp.content)
            return resp_json['media_id']

    def getMediaList(self, media_type, offset='0', count='20'):
        access_token = self.getAccessToken()
        url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % access_token
        data = {'type': media_type, 'offset': offset, 'count': count}
        print data
        resp = requests.post(url=url, data=data)
        print resp.content
        if resp.status_code == 200:
            resp_json = json.loads(resp.content)
            print resp_json['item']
            return 'success'

    def menuCreate(self):
        access_token = self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token
        data = {
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
        resp = requests.post(url=url, data=data)
        if resp.status_code == 200:
            print resp.content

if __name__ == '__main__':
    interface = Interface()
    print interface.getAccessToken()
    print interface.addMedia('app/static/qrcode.jpg', 'image', temp=False)
    print interface.getMediaList('image')
