# -*- coding: utf-8 -*-
from app import app
from flask import request, make_response
import hashlib
import sys

@app.route('/', methods = ['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'hellowode'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, s)
        hashcode = sha1.hexdigest()
        sys.stdout('aaa'+signature+hashcode)
        if hashcode == signature:
            return make_response(echostr)

