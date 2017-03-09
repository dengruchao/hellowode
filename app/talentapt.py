# -*- coding: utf-8 -*-
import requests
import json
from lxml import etree

class TalentApt:
    def __init__(self):
        self.session = requests.Session()

    def login(self):
        #url = 'http://www.zj-talentapt.com/Login.aspx?flag=0&userName=13166297263&passWord=ZHJjMzA2NDMz&md5=422fe37bc380cb48118133a7d17ae058'
        login_url = 'http://www.zj-talentapt.com/ashx/ApiService.ashx?url=/users/login'
        data = {"systemId":"ht_02","mobilePhone":"13166297263","accountType":"1","password":"422fe37bc380cb48118133a7d17ae058"}
        resp = self.session.post(url=login_url, data=data)
        print resp.content

    def getWaitingRecord(self):
        url = 'http://www.zj-talentapt.com/System/WaitingRecord.aspx'
        resp = self.session.get(url)
        html = etree.HTML(resp.text)
        num = html.xpath('//*[@id="ctl00_ctl00_ctl00_main_main_main_rptApplyRecord_ctl00_labPageRank"]/text()')[0]
        return num

talentapt = TalentApt()