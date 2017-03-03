# -*- coding: utf-8 -*-
from flask import make_response
import time

class Reply:

	def __init__(self):
		self.fromUserName = None
		self.toUserName = None

	def menu(self):
		content = u'请输入“文本”'
		return self.textMsg(self.fromUserName, self.toUserName, content)

	def textMsg(self, content):
		xml_rep = "<xml>\
					<ToUserName><![CDATA[%s]]></ToUserName>\
					<FromUserName><![CDATA[%s]]></FromUserName>\
					<CreateTime>%s</CreateTime>\
					<MsgType><![CDATA[text]]></MsgType>\
					<Content><![CDATA[%s]]></Content>\
					<FuncFlag>0</FuncFlag>\
					</xml>"
		response = make_response(xml_rep % (self.fromUserName, self.toUserName, str(int(time.time())), content))
		response.content_type = 'application/xml'
		return response

	def imageMsg(self):
		pass

	def dispatch(self, content):
		if content == u'文本':
			return self.textMsg(content)
		else:
			return self.menu()

reply = Reply()

