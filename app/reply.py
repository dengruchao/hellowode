# -*- coding: utf-8 -*-
from flask import make_response
import xml.etree.ElementTree as ET
import time
import json
import requests
from interface import Interface
from meizitu import Meizitu
from talentapt import TalentApt
from music import Music
from location import Location
# import pylibmc as memcache
from vip_vedio import VipVideo

class Reply:

    def __init__(self, fromUserName):
        self.fromUserName = None
        self.toUserName = None
        self.interface = Interface()
        self.meizitu = Meizitu()
        self.talentapt = TalentApt()
        self.music = Music()
        self.location = Location(fromUserName)
        self.vip_vedio = VipVideo()

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

    def musicMsg(self, link, name, singer):
        #link = 'http://music.163.com/#/song?id=436514312'
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
        response = make_response(xml_resp % (self.fromUserName, self.toUserName, str(int(time.time())), name, u'歌手：%s'%singer, link, link))
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

    def tulingRobot(self, content):
        userid = 0
        for chr in self.fromUserName:
            userid += ord(chr)

        url = 'http://www.tuling123.com/openapi/api'
        data = {'key': 'db0b623ae0dd4e9ca28a89174abe156c', 'info': content, 'userid': str(userid)}
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

    def dispatch(self, recv):
        xml_recv = ET.fromstring(recv)
        self.toUserName = xml_recv.find('ToUserName').text
        self.fromUserName = xml_recv.find('FromUserName').text
        msgType = xml_recv.find('MsgType').text
        if msgType == 'text':
            text = xml_recv.find('Content').text
            if text == u'文本':
                return self.textMsg(text)
            elif text.find(u'音乐') != -1:
                name = text.split(' ')[-1]
                link, name, singer = self.music.getMusic(name)
                return self.musicMsg(link, name, singer)
            elif text == u'二维码':
                # media_id = self.interface.addMedia('app/static/qrcode.jpg', 'image', 0)
                return self.imageMsg('a7Zzsef34bHTIphJVVhcc2fFZxqCt6gZO3HSuGHtu68')
            elif text == u'开始跑步':
                # mc = memcache.Client()
                # mc.set('running', True)
                return self.textMsg('奔跑吧，小伙')
            elif text == u'结束跑步':
                # mc = memcache.Client()
                # mc.set('running', False)
                distance = self.location.calDistance()
                self.location.cleanAllPoints()
                return self.textMsg(distance)
            elif text in self.meizitu.tag_list:
                articals = self.meizitu.crawl(self.meizitu.tag_list.index(text))
                return self.imgTextMsg(articals)
            elif text == u'人才公寓':
                self.talentapt.login()
                num, checked = self.talentapt.getWaitingRecord()
                text_reply = u'企业审核: %s\n当前排名: %s' % (checked, num)
                return self.textMsg(text_reply)
            elif text[0:5] == u'vip视频':
                return self.textMsg(self.vip_vedio.free_url(text[5:]))
            else:
                return self.tulingRobot(text)
        elif msgType == 'image':
            media_id = xml_recv.find('MediaId').text
            return self.imageMsg(media_id)
        elif msgType == 'event':
            event = xml_recv.find('Event').text
            if event == 'subscribe':
                return self.subscribe()
            elif event == 'LOCATION':
                # mc = memcache.Client()
                # running = mc.get('running')
                # if running:
                #     latitude = xml_recv.find('Latitude').text
                #     longitude = xml_recv.find('Longitude').text
                #     precision = xml_recv.find('Precision').text
                #     print latitude, longitude, precision
                #     self.location.addPoint(latitude, longitude)
                return 'success'
        else:
            return self.menu()


