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
					<MediaId><![CDATA[%d]]></MediaId>\
					</Image>\
					</xml>'
		response = make_response(xml_resp % (self.fromUserName, self.toUserName, str(int(time.time())), media_id))
		response.content_type = 'application/xml'
		return response

	def dispatch(self, msgType, content):
		if msgType == 'text':
			return self.textMsg(content)
		elif msgType == 'image':
			return self.imageMsg(content)
		else:
			return self.menu()

reply = Reply()

