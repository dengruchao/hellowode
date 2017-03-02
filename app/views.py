# -*- coding: utf-8 -*-
import time
from app import app
from flask import request, make_response
import hashlib
import xml.etree.ElementTree as ET

@app.route('/',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='liusicong'
        data = request.args
        signature = data.get('signature','')
        print 'signature', signature
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        print 'old', hashlib.sha1(s).hexdigest()
        #if (hashlib.sha1(s).hexdigest() == signature):
        #    return make_response(echostr)
        #else:
        #    return 'Hello World'
        list1=[token,timestamp,nonce]
        list1.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list1)
        hashcode=sha1.hexdigest()
        print 'new', hashcode
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        else:
            return 'HEl'
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())), content))
        response.content_type='application/xml'
        return response

