# -*- coding: utf-8 -*-
from reply import *
from lxml import etree
import re

class Meizitu:
	def __init__(self):
		self.url = 'http://www.meizitu.com/'

	def crawl(self, tag):
		resp = requests.get(self.url)
		resp.encoding = 'gb2312'
		page = resp.text
		pattern = '<span>.*?href="(.*?)".*?target="_blank".*?title="%s"' % tag
		link = re.search(pattern, page, re.S)
		print link.group(1)
		resp = requests.get(link.group(1))
		page = resp.content
		html = etree.HTML(page)
		articals = []
		for i in range(10):
			link = html.xpath('//*[@id="maincontent"]/div[1]/ul/li[%s]/div/div/a/@href' % i)[0]
			link_img = html.xpath('//*[@id="maincontent"]/div[1]/ul/li[%s]/div/div/a/img')[0]
			name = html.xpath('//*[@id="maincontent"]/div[1]/ul/li[%s]/div/div/a/img/@alt' % i)[0]
			articals.append([name, name, link_img, link])
		print articals
		return reply.imgTextMsg(articals)

meizitu = Meizitu()