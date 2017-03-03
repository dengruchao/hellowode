# -*- coding: utf-8 -*-
from flask import make_response
import time
from wechatInterface import wechatInterface

class Reply:

	def __init__(self):
		self.fromUserName = None
		self.toUserName = None

	def menu(self):
		content = u'请输入“文本”'
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
		link = 'http://m10.music.126.net/20170303190437/7577ba21915fffd1d3b2bdc098d0950b/ymusic/47fe/b7b0/059b/1527f518027a60ede32fd42f8f1762ab.mp3'
		xml_resp = '<xml>\
					<ToUserName><![CDATA[%s]]></ToUserName>\
					<FromUserName><![CDATA[%s]]></FromUserName>\
					<CreateTime>%s</CreateTime>\
					<MsgType><![CDATA[music]]></MsgType>\
					<Music>\
					<Title><![CDATA[%s]]></Title>\
					<Description><![CDATA[%s]]></Description>\
					<MusicUrl><![CDATA[%s]]></MusicUrl>\
					</Music>\
					</xml>'
		response = make_response(xml_resp % (self.fromUserName, self.toUserName, str(int(time.time())), u'彩虹', 'nothing', link))
		response.content_type = 'application/xml'
		return response

	def dispatch(self, msgType, content):
		if msgType == 'text':
			if content == u'文本':
				return self.textMsg(content)
			elif content == u'音乐':
				print 'ok'
				return self.musicMsg()
		elif msgType == 'image':
			return self.imageMsg(content)
		else:
			return self.menu()

reply = Reply()

