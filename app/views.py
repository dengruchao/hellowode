# -*- coding: utf-8 -*-
import time
from app import app
from flask import request, make_response
import hashlib
import xml.etree.ElementTree as ET

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
        toUserName = xml_recv.find('ToUserName').text
        fromUserName = xml_recv.find('FromUserName').text
        content = xml_recv.find('Content').text
        print content
        if content == u'文本':
            return textMsg(fromUserName, toUserName, content)
        else:
            return make_response('error')

def textMsg(fromUserName, toUserName, content):
    xml_rep = "<xml>\
                <ToUserName><![CDATA[%s]]></ToUserName>\
                <FromUserName><![CDATA[%s]]></FromUserName>\
                <CreateTime>%s</CreateTime>\
                <MsgType><![CDATA[text]]></MsgType>\
                <Content><![CDATA[%s]]></Content>\
                <FuncFlag>0</FuncFlag>\
                </xml>"
    response = make_response(xml_rep % (fromUserName, toUserName, str(int(time.time())), content))
    response.content_type = 'application/xml'
    return response
