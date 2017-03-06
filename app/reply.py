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

	def dispatch(self, msgType, content):
		if msgType == 'text':
			if content == u'文本':
				return self.textMsg(content)
			elif content == u'音乐':
				return self.musicMsg()
			elif content == u'图文':
				item_list = [[u'一大波美女即将来袭', u'纯美的女子，结白的内衣写真', 'http://mm.howkuai.com/wp-content/uploads/2017a/03/01/01.jpg', 'http://www.baidu.com'],
				             [u'一大波美女即将来袭', u'纯美的女子，结白的内衣写真', 'http://mm.howkuai.com/wp-content/uploads/2017a/03/01/02.jpg', 'http://www.baidu.com']]
				return self.imgTextMsg(item_list)
			elif content == u'菜单':
				content = wechatInterface.menuCreate()
				response = make_response(content)
				response.content_type = 'text'
				return response
		elif msgType == 'image':
			return self.imageMsg(content)
		else:
			return self.menu()

reply = Reply()

