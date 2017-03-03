# -*- coding: utf-8 -*-
from app import app
from flask import request, make_response
import hashlib
import xml.etree.ElementTree as ET
from reply import reply

@app.route('/', methods = ['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token ='liusicong'
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
        rec = request.stream.read()
        xml_recv = ET.fromstring(rec)
        reply.toUserName = xml_recv.find('ToUserName').text
        reply.fromUserName = xml_recv.find('FromUserName').text
        content = xml_recv.find('Content').text
        return reply.dispatch(content)

