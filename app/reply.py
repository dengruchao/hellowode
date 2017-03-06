# -*- coding: utf-8 -*-
from flask import make_response
import time
from wechatInterface import *
from meizitu import *

class Reply:

	def __init__(self):
		self.fromUserName = None
		self.toUserName = None
		self.tag_list = [u'性感', u'浴室', u'私房', u'美腿', u'清纯', u'甜美', u'治愈系', u'萌妹子', u'小清新', u'女神', u'气质美女', u'嫩模', u'车模', u'比基尼', u'足球宝贝', u'萝莉', u'90后', u'日韩美女']

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
				#resp2 = requests.get(news['detailurl'])
				#html = etree.HTML(resp2.content)
				#try:
				#	img_url = html.xpath('//*[@id="endText"]/p[1]/img/@src')[0]
				#except:
				img_url = 'http://imgsrc.baidu.com/forum/w=580/sign=deeeda7249c2d562f208d0e5d71090f3/618cd609b3de9c82b68e8d9d6a81800a18d84309.jpg'
				item = [news['article'], news['source'], img_url, news['detailurl']]
				item_list.append(item)
				if len(item_list) == 10:
					break
			print item_list
			return self.imgTextMsg(item_list)

	def dispatch(self, msgType, content):
		if msgType == 'text':
			if content == u'文本':
				return self.textMsg(content)
			elif content == u'音乐':
				return self.musicMsg()
			elif content in self.tag_list:
				articals = meizitu.crawl(self.tag_list.index(content))
				return self.imgTextMsg(articals)
			else:
				return self.tulingRobot(content)
		elif msgType == 'image':
			return self.imageMsg(content)
		elif msgType == 'event':
			return self.subscribe()
		else:
			return self.menu()

reply = Reply()

