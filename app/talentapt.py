# -*- coding: utf-8 -*-
import requests
from lxml import etree
import json
import hashlib
import base64

class TalentApt:
    def __init__(self):
        self.session = requests.Session()

    def login(self):
        #url = 'http://www.zj-talentapt.com/Login.aspx?flag=0&userName=13166297263&passWord=ZHJjMzA2NDMz&md5=422fe37bc380cb48118133a7d17ae058'
        #resp = self.session.get(url)
        url = 'http://rcgy.zjhui.net/ashx/ApiService.ashx'
        payload = {
                'data': '{"systemId":"ht_02","mobilePhone":"17521084212","accountType":"1","password":"5d93ceb70e2bf5daa84ec3d0cd2c731a"}',
                'url': '/users/login'
                }
        self.headers = {
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Connection':'keep-alive',
                'Content-Length':'160',
                'Content-Type':'application/json; charset=UTF-8',
                # 'Cookie':'ASP.NET_SessionId=gw5pje45nd4hg0ix351bna45; safedog-flow-item=',
                'Host':'rcgy.sh-zj.gov.cn',
                'Origin':'https://rcgy.sh-zj.gov.cn',
                'Referer':'https://rcgy.sh-zj.gov.cn/',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest',
                }
        resp = self.session.post(url, headers=self.headers, data=json.dumps(payload), verify=False)
        username = '17521084212'
        password = 'qwer1234'
        password_base64 = base64.b64encode(password)
        password_md5    = hashlib.md5(password).hexdigest()
        url ='http://rcgy.zjhui.net/Login.aspx?flag=0&userName=%s&passWord=%s&md5=%s' % (username, password_base64, password_md5)
        resp = self.session.get(url, headers=self.headers, verify=False)
        if resp.url == 'https://rcgy.sh-zj.gov.cn/Default.aspx':
            print 'login successful'
        else:
            print 'login failed', resp.url

    def getWaitingRecord(self):
        #url = 'http://www.zj-talentapt.com/System/WaitingRecord.aspx'
        url = 'https://rcgy.sh-zj.gov.cn/System/WaitingRecord.aspx'
        self.headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Connection':'keep-alive',
                #'Cookie':'ASP.NET_SessionId=bqxhku45xisqr445bnrxld2n',
                'Host':'rcgy.sh-zj.gov.cn',
                'Referer':'https://rcgy.sh-zj.gov.cn/System/ApplyRecord.aspx',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                }
        resp = self.session.get(url, headers=self.headers)
        html = etree.HTML(resp.text)
        num = html.xpath('//span[@id="ctl00_ctl00_ctl00_main_main_main_rptPtApplyRecord_ctl00_labPageRank"]/text()')[0]
        checked = html.xpath('//*[@id="ctl00_ctl00_ctl00_main_main_main_palPT"]/table/tbody/tr[2]/td[9]/text()')[0].strip()
        return num, checked

if __name__ == '__main__':
    talentapt = TalentApt()
    talentapt.login()
    print talentapt.getWaitingRecord()

