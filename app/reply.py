# -*- coding: utf-8 -*-
from flask import make_response
import time
from wechatInterface import *
from meizitu import *
from talentapt import talentapt

class Reply:

    def __init__(self):
        self.fromUserName = None
        self.toUserName = None

    def menu(self):
        content = u'你好，我现在还不知道怎么处理这个消息'
        return self.textMsg(content)

    def textMsg(self, content):
        xml_resp = "<xml>\
                    <ToUserName><![CDATA[%s]]></ToUserName>\
                    <FromUserName><![CDATA[%s]]></FromUserName>\
                    <CreateTime>%s</CreateTime>\
                    <MsgType><![CDATA[text]]></MsgType>\
                    <Content><![CDATA[%s]]></Content>\
                    <FuncFlag>0</FuncFlag>\
                    </xml>"
        response = make_response(xml_resp % (self.fromUserName, self.toUserName, str(int(time.time())), content))
        response.content_type = 'application/xml'
        return response

    def imageMsg(self, media_id):
        xml_resp = '<xml>\
                    <ToUserName><![CDATA[%s]]></ToUserName>\
                    <FromUserName><![CDATA[%s]]></FromUserName>\
                    <CreateTime>%s</CreateTime>\
                    <MsgType><![CDATA[image]]></MsgType>\
                    <Image>\
                    <MediaId><![CDATA[%s]]></MediaId>\
                    </Image>\
                    </xml>'
        response = make_response(xml_resp % (self.fromUserName, self.toUserName, str(int(time.time())), media_id))
        response.content_type = 'application/xml'
        return response

    def musicMsg(self):
        link = 'http://mascot-music.stor.sinaapp.com/zxmzf.mp3'
        xml_resp = '<xml>\
                    <ToUserName><![CDATA[%s]]></ToUserName>\
                    <FromUserName><![CDATA[%s]]></FromUserName>\
                    <CreateTime>%s</CreateTime>\
                    <MsgType><![CDATA[music]]></MsgType>\
                    <Music>\
                    <Title><![CDATA[%s]]></Title>\
                    <Description><![CDATA[%s]]></Description>\
                    <MusicUrl><![CDATA[%s]]></MusicUrl>\
                    <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>\
                    </Music>\
                    </xml>'
        response = make_response(xml_resp % (self.fromUserName, self.toUserName, str(int(time.time())), u'最炫民族风', u'歌手：凤凰传奇', link, link))
        response.content_type = 'application/xml'
        return response

    def imgTextMsg(self, item_list):
        item_fmt = '<item>\
                    <Title><![CDATA[%s]]></Title>\
                    <Description><![CDATA[%s]]></Description>\
                    <PicUrl><![CDATA[%s]]></PicUrl>\
                    <Url><![CDATA[%s]]></Url>\
                    </item>'
        item_xml_list = []
        for item in item_list:
            item_xml = item_fmt % (item[0], item[1], item[2], item[3])
            item_xml_list.append(item_xml)

        xml_resp = '<xml>\
                    <ToUserName><![CDATA[%s]]></ToUserName>\
                    <FromUserName><![CDATA[%s]]></FromUserName>\
                    <CreateTime>%s</CreateTime>\
                    <MsgType><![CDATA[news]]></MsgType>\
                    <ArticleCount>%d</ArticleCount>\
                    <Articles>\
                    %s\
                    </Articles>\
                    </xml>'
        response = make_response(xml_resp % (self.fromUserName, self.toUserName, str(int(time.time())), len(item_list), '\n'.join(item_xml_list)))
        response.content_type = 'application/xml'
        return response

    def subscribe(self):
        content = u'欢迎来到邓小超的微信公众号'
        return self.textMsg(content)

    def tulingRobot(self,content):
        url = 'http://www.tuling123.com/openapi/api'
        data = {'key': 'db0b623ae0dd4e9ca28a89174abe156c', 'info': content, 'userid': '123456'}
        resp = requests.post(url, data=data)
        resp_json = json.loads(resp.content)
        code = resp_json['code']
        if code == 100000:
            return self.textMsg(resp_json['text'])
        elif code == 200000:
            return self.textMsg(resp_json['text']+'\n'+resp_json['url'])
        elif code == 302000:
            item_list = []
            for news in resp_json['list']:
                item = [news['article'], news['source'], news['icon'], news['detailurl']]
                item_list.append(item)
                if len(item_list) == 5:
                    break
            return self.imgTextMsg(item_list)
        elif code == 308000:
            item_list = []
            for menu in resp_json['list']:
                item = [menu['name'], menu['info'], menu['icon'], menu['detailurl']]
                item_list.append(item)
                if len(item_list) == 5:
                    break
            return self.imgTextMsg(item_list)

    def dispatch(self, msgType, content):
        if msgType == 'text':
            if content == u'文本':
                return self.textMsg(content)
            elif content == u'音乐':
                return self.musicMsg()
            elif content == u'二维码':
                print self.fromUserName
                media_id = wechatInterface.addMedia('app/static/qrcode.jpg', 'image', 0)
                return self.imageMsg(media_id)
            elif content in meizitu.tag_list:
                articals = meizitu.crawl(meizitu.tag_list.index(content))
                return self.imgTextMsg(articals)
            elif content == u'人才公寓':
                talentapt.login()
                num = talentapt.getWaitingRecord()
                return self.textMsg(num)
            else:
                return self.tulingRobot(content)
        elif msgType == 'image':
            return self.imageMsg(content)
        elif msgType == 'event':
            return self.subscribe()
        else:
            return self.menu()

reply = Reply()

