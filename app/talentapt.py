# -*- coding: utf-8 -*-
import requests

class TalentApt:
    def __init__(self):
        self.session = requests.Session()

    def login(self):
        login_url = 'http://www.zj-talentapt.com/ashx/ApiService.ashx?url=/users/login'
        data = {"systemId":"ht_02","mobilePhone":"13166297263","accountType":"1","password":"422fe37bc380cb48118133a7d17ae058"}
        resp = self.session.post(url=login_url, data=data)
        print resp

talentapt = TalentApt()