# -*- coding: utf-8 -*-
from app import app
from flask import request, make_response
import hashlib
from reply import Reply
import xml.etree.ElementTree as ET

@app.route('/', methods = ['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token ='dengruchao'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        list1 = [token, timestamp, nonce]
        list1.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list1)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            response = make_response(echostr)
            response.content_type = 'text'
            return response
        else:
            return 'Hello World'
    else:
        recv = request.stream.read()
        xml_recv = ET.fromstring(recv)
        fromUserName = xml_recv.find('FromUserName').text
        reply = Reply(fromUserName)
        return reply.dispatch(recv)

