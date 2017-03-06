# -*- coding: utf-8 -*-
from reply import *
from lxml import etree
import re

class Meizitu:
	def __init__(self):
		self.url = 'http://www.meizitu.com/'

	def crawl(self, tag_index):
		resp = requests.get(self.url)
		resp.encoding = 'gb2312'
		page = resp.text
		html = etree.HTML(page)
		path = '//*[@id="subcontent clearfix"]/div[2]/span/a[%d]/@href' % (tag_index+1)
		tag_url = html.xpath(path)[0]
		print tag_url
		resp = requests.get(tag_url)
		page = resp.content
		html = etree.HTML(page)
		articals = []
		for i in range(10):
			link_p = '//*[@id="maincontent"]/div[1]/ul/li[%d]/div/div/a/@href' % (i+1)
			link = html.xpath(link_p)[0]
			link_img_p = '//*[@id="maincontent"]/div[1]/ul/li[%d]/div/div/a/img' % (i+1)
			link_img = html.xpath(link_img_p)[0]
			name_p = '//*[@id="maincontent"]/div[1]/ul/li[%d]/div/div/a/img/@alt' % (i+1)
			name = html.xpath(name_p)[0]
			articals.append([name, name, link_img, link])
		return articals

meizitu = Meizitu()